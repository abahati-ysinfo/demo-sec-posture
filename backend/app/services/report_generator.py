import asyncio
import logging
import random
import time
import uuid
from datetime import UTC, datetime
from typing import Any

import markdown2  # type: ignore[import-untyped]
from jinja2 import Environment
from openai import (
    APIConnectionError,
    APIError,
    AsyncOpenAI,
    AuthenticationError,
    OpenAI,
    OpenAIError,
    RateLimitError,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from weasyprint import HTML

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.scoring_scales import (
    get_option_weight,
    map_numeric_to_slug,
    normalize_option_value,
)
from app.models.ai_artifacts import AISectionArtifact as AISectionArtifactModel
from app.models.ai_artifacts import AISynthesisArtifact as AISynthesisArtifactModel
from app.models.ai_metadata import AIGenerationMetadata
from app.models.assessment import Assessment, AssessmentResponse, Report
from app.schemas.ai_artifacts import (
    Benchmark,
    Gap,
    Recommendation,
    SectionAIArtifact,
    SynthesisArtifact,
)
from app.schemas.assessment import Question
from app.services.ai_cache import AICacheService
from app.services.ai_synthesis import (
    create_minimal_synthesis,
    generate_synthesis_artifact,
)
from app.services.benchmark_context import benchmark_context_service
from app.services.enhanced_context_extractor import get_enhanced_context_extractor
from app.services.enhanced_executive_summary import (
    generate_enhanced_executive_summary,
)
from app.services.openai_key_manager import OpenAIKeyManager
from app.services.pii_redactor import PIIRedactor
from app.services.prompt_builder import build_section_prompt_v2
from app.services.question_parser import (
    filter_structure_by_sections,
    load_assessment_structure,
)
from app.services.security_metrics import security_metrics
from app.services.storage import get_storage_service
from app.utils.openai_helpers import get_token_params

logger = logging.getLogger(__name__)

jinja_env = Environment(autoescape=True)


def markdown_filter(text: str | None) -> str:
    """Convert markdown to HTML"""
    if not text:
        return ""
    result: str = markdown2.markdown(text, extras=["fenced-code-blocks", "tables"])
    return result


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type((Exception,)),
    reraise=True,
)
def generate_standard_report(report_id: str) -> None:
    """Generate a standard PDF report"""

    db = SessionLocal()
    report = None
    try:
        logger.info(f"Starting standard report generation for report_id: {report_id}")

        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            logger.error(f"Report not found: {report_id}")
            return

        assessment = (
            db.query(Assessment).filter(Assessment.id == report.assessment_id).first()
        )
        if not assessment:
            logger.error(f"Assessment not found for report: {report_id}")
            report.status = "failed"  # type: ignore[assignment]
            db.commit()
            return

        logger.info(f"Loading responses for assessment: {assessment.id}")
        responses = (
            db.query(AssessmentResponse)
            .filter(AssessmentResponse.assessment_id == assessment.id)
            .all()
        )
        logger.info(f"Found {len(responses)} responses")

        logger.info("Loading assessment structure")
        structure = load_assessment_structure()

        if assessment.selected_section_ids:
            logger.info(
                f"Filtering structure to {len(assessment.selected_section_ids)} selected sections"
            )
            structure = filter_structure_by_sections(
                structure,
                list(assessment.selected_section_ids),  # type: ignore[arg-type]
            )

        logger.info("Calculating scores")
        scores = calculate_assessment_scores(responses, structure)

        logger.info("Generating HTML content")
        html_content = generate_report_html(assessment, responses, scores, structure)
        logger.info(f"HTML content generated successfully ({len(html_content)} bytes)")

        filename = f"report_{report_id}_{uuid.uuid4().hex[:8]}.pdf"
        storage_service = get_storage_service()

        logger.info("REPORTS_DIR configured as: %s", settings.REPORTS_DIR)
        logger.info("Generating PDF bytes for storage")
        try:
            pdf_bytes = HTML(string=html_content, url_fetcher=None).write_pdf()
            logger.info("WeasyPrint PDF byte generation completed")
        except Exception as pdf_error:
            logger.error(
                "WeasyPrint PDF generation failed: %s", str(pdf_error), exc_info=True
            )
            raise

        logger.info("Saving report to configured storage backend")
        storage_location = storage_service.save(pdf_bytes, filename)

        if not storage_service.exists(storage_location):
            raise Exception(
                f"PDF file was not persisted at storage location {storage_location}"
            )

        logger.info("PDF generated and stored successfully: %s", storage_location)
        report.file_path = storage_location  # type: ignore[assignment]
        report.status = "completed"  # type: ignore[assignment]
        report.completed_at = datetime.now(UTC)  # type: ignore[assignment]
        db.commit()

        logger.info(
            f"Report generation completed successfully for report_id: {report_id}"
        )

    except Exception as e:
        error_msg = f"Error generating standard report {report_id}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        if report:
            report.status = "failed"  # type: ignore[assignment]
            db.commit()
    finally:
        db.close()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type((Exception,)),
    reraise=True,
)
def generate_ai_report(report_id: str) -> None:
    """Generate an AI-enhanced report using ChatGPT"""

    db = SessionLocal()
    report = None
    key_manager = None
    try:
        logger.info(f"Starting AI report generation for report_id: {report_id}")

        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            logger.error(f"Report not found: {report_id}")
            return

        key_manager = OpenAIKeyManager(db)

        assessment = (
            db.query(Assessment).filter(Assessment.id == report.assessment_id).first()
        )
        if not assessment:
            logger.error(f"Assessment not found for report: {report_id}")
            report.status = "failed"  # type: ignore[assignment]
            db.commit()
            return

        logger.info(f"Loading responses for assessment: {assessment.id}")
        responses = (
            db.query(AssessmentResponse)
            .filter(AssessmentResponse.assessment_id == assessment.id)
            .all()
        )
        logger.info(f"Found {len(responses)} responses")

        logger.info("Loading assessment structure")
        structure = load_assessment_structure()

        if assessment.selected_section_ids:
            logger.info(
                f"Filtering structure to {len(assessment.selected_section_ids)} selected sections"
            )
            structure = filter_structure_by_sections(
                structure,
                list(assessment.selected_section_ids),  # type: ignore[arg-type]
            )

        logger.info("Generating AI insights with parallel processing")
        ai_insights = asyncio.run(
            generate_ai_insights_async(
                responses, structure, key_manager, str(report.id)
            )
        )

        logger.info("Calculating scores")
        scores = calculate_assessment_scores(responses, structure)

        logger.info("Generating cross-section synthesis")
        try:
            synthesis_artifact = asyncio.run(
                generate_synthesis_artifact(
                    ai_insights, structure, scores, key_manager, db
                )
            )
        except Exception as e:
            logger.error(
                f"Cross-section synthesis failed; using minimal fallback: {e}",
                exc_info=True,
            )
            try:
                synthesis_artifact = create_minimal_synthesis(
                    scores["overall"]["percentage"]
                )
            except ValidationError:
                logger.warning(
                    "create_minimal_synthesis did not meet schema; generating compliant placeholder"
                )
                overall_score = scores["overall"]["percentage"]
                if overall_score >= 80:
                    risk_level = "Low"
                elif overall_score >= 60:
                    risk_level = "Medium"
                elif overall_score >= 40:
                    risk_level = "Medium-High"
                else:
                    risk_level = "High"

                synthesis_artifact = SynthesisArtifact(
                    executive_summary=(
                        f"Based on an overall security score of {overall_score:.1f}%, "
                        "this automated fallback executive summary provides a conservative synthesis "
                        "of the organization's security posture. The assessment highlights the need for "
                        "targeted improvements across core security domains including identity and access "
                        "management, data protection, incident response, and infrastructure security. "
                        "Key recommendations prioritize foundational controls while planning for strategic "
                        "enhancements in detection capabilities, response procedures, and governance frameworks. "
                        "This placeholder text ensures report deliverability when AI synthesis services are "
                        "temporarily unavailable and should be supplemented with detailed manual review."
                    ),
                    overall_risk_level=risk_level,  # type: ignore[arg-type]
                    overall_risk_explanation=(
                        "Automated fallback synthesis is being used due to temporary unavailability of AI services. "
                        "While section-level analyses provide valuable insights into specific security domains, "
                        "detailed cross-domain relationship analysis, initiative sequencing, and strategic roadmap "
                        "development would benefit from full AI synthesis capabilities and expert security review."
                    ),
                    cross_cutting_themes=[],
                    top_10_initiatives=[],
                    quick_wins=[],
                    long_term_strategy=(
                        "Adopt a phased, risk-based security roadmap aligned with industry best practices. "
                        "Phase 1 (0-3 months): Stabilize foundational controls including identity and access "
                        "management, patch management, configuration baselines, and backup resilience. "
                        "Phase 2 (3-6 months): Mature detection and response capabilities with improved visibility, "
                        "alert triage automation, incident playbooks, and regular tabletop exercises. "
                        "Phase 3 (6-12 months): Elevate data protection and cloud governance while integrating "
                        "continuous improvement loops, security metrics tracking, and executive KPI dashboards "
                        "for sustained security posture gains and regulatory compliance."
                    ),
                    confidence_score=0.5,
                )

        logger.info("Storing synthesis artifact")
        try:
            db_synthesis = AISynthesisArtifactModel(
                report_id=report.id,
                artifact_json=synthesis_artifact.model_dump(),
                prompt_version=settings.AI_PROMPT_VERSION,
                schema_version=settings.AI_SCHEMA_VERSION,
                model=settings.OPENAI_MODEL,
            )
            db.add(db_synthesis)
            db.commit()
        except SQLAlchemyError as e:
            logger.warning(f"Failed to persist synthesis artifact: {e}")
            db.rollback()

        logger.info("Generating enhanced executive summary")
        try:
            enhanced_summary = asyncio.run(
                generate_enhanced_executive_summary(
                    section_artifacts=ai_insights,
                    synthesis_artifact=synthesis_artifact,
                    scores=scores,
                    structure=structure,
                    assessment=assessment,
                    key_manager=key_manager,
                    db=db,
                )
            )
            synthesis_artifact.executive_summary = enhanced_summary
            logger.info(
                f"Enhanced executive summary generated ({len(enhanced_summary)} chars)"
            )
        except Exception as e:
            logger.warning(
                f"Failed to generate enhanced executive summary, using original: {e}"
            )

        logger.info("Generating AI report HTML with synthesis")
        html_content = generate_ai_report_html(
            assessment, responses, scores, structure, ai_insights, synthesis_artifact
        )

        filename = f"ai_report_{report_id}_{uuid.uuid4().hex[:8]}.pdf"
        storage_service = get_storage_service()

        logger.info("Generating AI PDF bytes")
        pdf_bytes = HTML(string=html_content, url_fetcher=None).write_pdf()

        logger.info("Saving AI report to configured storage backend")
        storage_location = storage_service.save(pdf_bytes, filename)

        if not storage_service.exists(storage_location):
            raise Exception(
                f"AI PDF file was not persisted at storage location {storage_location}"
            )

        import os

        fly_region = os.getenv("FLY_REGION", "unknown")
        fly_primary = os.getenv("FLY_PRIMARY_REGION", "unknown")
        storage_backend = getattr(settings, "STORAGE_BACKEND", "local")

        logger.info(
            f"AI PDF generated successfully: {storage_location} "
            f"(region={fly_region}, primary={fly_primary}, backend={storage_backend})"
        )
        report.file_path = storage_location  # type: ignore[assignment]
        report.status = "completed"  # type: ignore[assignment]
        report.completed_at = datetime.now(UTC)  # type: ignore[assignment]
        db.commit()

        logger.info(
            f"AI report generation completed successfully for report_id: {report_id} "
            f"with file_path: {storage_location}"
        )

    except Exception as e:
        error_msg = f"Error generating AI report {report_id}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        if report:
            report.status = "failed"  # type: ignore[assignment]
            db.commit()
    finally:
        db.close()


def calculate_assessment_scores(
    responses: list[AssessmentResponse], structure: Any
) -> dict[str, Any]:
    """Calculate assessment scores by section"""

    scores: dict[str, Any] = {
        "scoring_version": "v2" if settings.SCORING_V2_ENABLED else "v1",
        "question_library_version": settings.QUESTION_LIBRARY_VERSION,
    }
    response_dict = {r.question_id: r for r in responses}

    for section in structure.sections:
        section_score = 0
        section_max_score = 0
        section_responses = 0
        section_unknown_count = 0
        section_na_count = 0

        for question in section.questions:
            response = response_dict.get(question.id)
            if response:
                section_responses += 1

                if settings.SCORING_V2_ENABLED:
                    result = calculate_question_score_v2(response, question)
                    section_score += result["score"]
                    section_max_score += result["max_score"]

                    if "unknown" in result["flags"]:
                        section_unknown_count += 1
                    if "not_applicable" in result["flags"]:
                        section_na_count += 1
                else:
                    question_score = calculate_question_score(response, question)
                    section_score += question_score
                    section_max_score += question.weight
            else:
                section_max_score += question.weight

        completion_rate = (
            (section_responses / len(section.questions)) * 100
            if section.questions
            else 0
        )
        score_percentage = (
            (section_score / section_max_score) * 100 if section_max_score > 0 else 0
        )

        scores[section.id] = {  # type: ignore[assignment]
            "score": section_score,
            "max_score": section_max_score,
            "percentage": score_percentage,
            "completion_rate": completion_rate,
            "responses_count": section_responses,
            "total_questions": len(section.questions),
            "unknown_count": section_unknown_count,
            "not_applicable_count": section_na_count,
        }

    from collections.abc import Mapping
    from typing import cast

    dict_scores: list[Mapping[str, Any]] = [
        cast(Mapping[str, Any], s) for s in scores.values() if isinstance(s, dict)
    ]
    total_score = sum(s["score"] for s in dict_scores if "score" in s)
    total_max_score = sum(s["max_score"] for s in dict_scores if "max_score" in s)
    total_unknown = sum(
        s.get("unknown_count", 0) for s in dict_scores if "unknown_count" in s
    )
    total_na = sum(
        s.get("not_applicable_count", 0)
        for s in dict_scores
        if "not_applicable_count" in s
    )

    overall_percentage = (
        (total_score / total_max_score) * 100 if total_max_score > 0 else 0
    )

    scores["overall"] = {  # type: ignore[assignment]
        "score": total_score,
        "max_score": total_max_score,
        "percentage": overall_percentage,
        "unknown_count": total_unknown,
        "not_applicable_count": total_na,
    }

    return scores


def calculate_question_score(response: AssessmentResponse, question: Any) -> int:
    """Calculate score for a single question response"""

    if question.type == "yes_no":
        if response.answer_value == "yes":
            return int(question.weight)
        else:
            return 0

    elif question.type == "multiple_choice":
        return question.weight if response.answer_value else 0

    elif question.type == "multiple_select":
        if isinstance(response.answer_value, list):
            return question.weight if response.answer_value else 0
        return question.weight if response.answer_value else 0

    return 0


def calculate_question_score_v2(
    response: AssessmentResponse, question: Any
) -> dict[str, Any]:
    """Calculate score with v2 weighted logic"""

    answer = response.answer_value
    flags: list[str] = []

    if question.type == "yes_no":
        score = question.weight if answer == "yes" else 0
        return {"score": score, "max_score": question.weight, "flags": flags}

    elif question.type == "multiple_choice":
        scale_type = question.scale_type
        if scale_type:
            mapped_answer = map_numeric_to_slug(question, str(answer))
            normalized_answer = normalize_option_value(mapped_answer)
            weight_multiplier, answer_flags = get_option_weight(
                scale_type, normalized_answer
            )
            flags.extend(answer_flags)

            if "not_applicable" in flags:
                return {"score": 0, "max_score": 0, "flags": flags}

            score = int(question.weight * weight_multiplier)
            return {"score": score, "max_score": question.weight, "flags": flags}
        else:
            score = question.weight if answer else 0
            return {"score": score, "max_score": question.weight, "flags": flags}

    elif question.type == "multiple_select":
        if not isinstance(answer, list):
            answer = [answer] if answer else []  # type: ignore[assignment]

        if not answer:
            return {"score": 0, "max_score": question.weight, "flags": flags}

        scale_type = question.scale_type
        if scale_type:
            best_weight = 0
            all_flags = []

            for selected_value in list(answer):
                mapped_value = map_numeric_to_slug(question, str(selected_value))
                normalized = normalize_option_value(mapped_value)
                weight, value_flags = get_option_weight(scale_type, normalized)
                all_flags.extend(value_flags)
                best_weight = max(best_weight, weight)  # type: ignore[assignment]

            if "not_applicable" in all_flags:
                return {"score": 0, "max_score": 0, "flags": all_flags}

            score = int(question.weight * best_weight)
            return {"score": score, "max_score": question.weight, "flags": all_flags}
        else:
            score = question.weight
            return {"score": score, "max_score": question.weight, "flags": flags}

    return {"score": 0, "max_score": question.weight, "flags": flags}


def generate_ai_insights(
    responses: list[AssessmentResponse],
    structure: Any,
    key_manager: OpenAIKeyManager,
    report_id: str,
    db: Any,
) -> dict[str, SectionAIArtifact]:
    """Generate AI insights for each section using JSON mode with structured output"""

    insights = {}
    response_dict = {r.question_id: r for r in responses}
    cache_service = AICacheService()

    try:
        key_id, api_key = key_manager.get_next_key()
        client = OpenAI(api_key=api_key, timeout=settings.OPENAI_TIMEOUT)
        logger.info(f"Using API key {key_id} for AI report generation")
    except ValueError as e:
        logger.error(f"Failed to get OpenAI API key: {e}")
        raise

    extractor = get_enhanced_context_extractor()
    pii_redactor = PIIRedactor() if settings.ENABLE_PII_REDACTION_BEFORE_AI else None
    total_redactions = 0

    for section in structure.sections:
        section_responses = []
        for question in section.questions:
            response = response_dict.get(question.id)
            if response:
                answer_value = response.answer_value
                comment_value = response.comment if response.comment else None

                if pii_redactor:
                    answer_str = str(answer_value) if answer_value else ""
                    redacted_answer_str, answer_redaction_count = pii_redactor.redact(
                        answer_str
                    )
                    if answer_redaction_count > 0:
                        total_redactions += answer_redaction_count
                        logger.info(
                            f"PII redacted in answer for question {question.id} ({answer_redaction_count} items)"
                        )
                    answer_value = redacted_answer_str  # type: ignore[assignment]

                    if comment_value:
                        redacted_comment, comment_redaction_count = pii_redactor.redact(
                            str(comment_value)
                        )
                        if comment_redaction_count > 0:
                            total_redactions += comment_redaction_count
                            logger.info(
                                f"PII redacted in comment for question {question.id} ({comment_redaction_count} items)"
                            )
                        comment_value = redacted_comment  # type: ignore[assignment]

                resp_dict = {
                    "question": question.text,
                    "answer": answer_value,
                    "weight": question.weight,
                }

                if settings.INCLUDE_COMMENTS_IN_AI and comment_value:
                    resp_dict["comment"] = comment_value

                if settings.INCLUDE_ENHANCED_CONTEXT_IN_AI:
                    context = extractor.get_compact_context(
                        question.id,
                        str(response.answer_value),
                        max_chars=settings.MAX_CONTEXT_CHARS,
                        question_options=question.options,
                    )
                    if context:
                        if pii_redactor:
                            redacted_context, context_redaction_count = (
                                pii_redactor.redact(context)
                            )
                            if context_redaction_count > 0:
                                total_redactions += context_redaction_count
                                logger.info(
                                    f"PII redacted in context for question {question.id} ({context_redaction_count} items)"
                                )
                            context = redacted_context
                        resp_dict["context"] = context

                section_responses.append(resp_dict)

        if section_responses:
            retry_attempted = False
            max_retries = 1  # Single retry for transient errors

            for attempt in range(max_retries + 1):
                try:
                    answers_hash = cache_service.compute_answers_hash(section_responses)

                    cached_artifact = cache_service.get_cached_artifact(
                        db,
                        section.id,
                        answers_hash,
                        settings.AI_PROMPT_VERSION,
                        settings.OPENAI_MODEL,
                    )

                    if cached_artifact:
                        db_artifact = AISectionArtifactModel(
                            report_id=report_id,
                            section_id=section.id,
                            artifact_json=cached_artifact.model_dump(),
                        )
                        db.add(db_artifact)
                        db.commit()

                        insights[section.id] = cached_artifact
                        break  # Success, exit retry loop

                    curated_context = benchmark_context_service.get_relevant_context(
                        section.title, section.description, max_controls=5
                    )
                    prompt, redaction_count = build_section_prompt_v2(
                        section, section_responses, curated_context
                    )

                    start_time = datetime.now()
                    response = client.chat.completions.create(  # type: ignore[assignment]  # type: ignore[assignment]
                        model=settings.OPENAI_MODEL,
                        messages=[{"role": "user", "content": prompt}],
                        response_format={"type": "json_object"},
                        temperature=settings.OPENAI_TEMPERATURE,
                        **get_token_params(settings.OPENAI_MAX_TOKENS),
                    )
                    end_time = datetime.now()

                    if not response or not response.choices:
                        raise ValueError("Empty response from OpenAI API")

                    json_str = response.choices[0].message.content
                    artifact = safe_validate_section_artifact(json_str, section.id)

                    db_artifact = AISectionArtifactModel(
                        report_id=report_id,
                        section_id=section.id,
                        artifact_json=artifact.model_dump(),
                    )
                    db.add(db_artifact)

                    tokens_prompt = (
                        response.usage.prompt_tokens if response.usage else 0
                    )
                    tokens_completion = (
                        response.usage.completion_tokens if response.usage else 0
                    )
                    finish_reason = (
                        response.choices[0].finish_reason if response.choices else None
                    )
                    cost_usd = (
                        (tokens_prompt * 0.00001 + tokens_completion * 0.00003)
                        if response.usage
                        else 0.0
                    )

                    logger.info(
                        f"Section {section.id}: finish_reason={finish_reason}, "
                        f"tokens={tokens_prompt}+{tokens_completion}={tokens_prompt + tokens_completion}"
                    )

                    metadata = AIGenerationMetadata(
                        report_id=report_id,
                        section_id=section.id,
                        prompt_version=settings.AI_PROMPT_VERSION,
                        schema_version=settings.AI_SCHEMA_VERSION,
                        model=settings.OPENAI_MODEL,
                        temperature=settings.OPENAI_TEMPERATURE,
                        max_tokens=settings.OPENAI_MAX_TOKENS,
                        tokens_prompt=tokens_prompt,
                        tokens_completion=tokens_completion,
                        finish_reason=finish_reason,
                        total_cost_usd=cost_usd,
                        latency_ms=int((end_time - start_time).total_seconds() * 1000),
                    )
                    db.add(metadata)

                    cache_service.store_artifact(
                        db,
                        section.id,
                        answers_hash,
                        settings.AI_PROMPT_VERSION,
                        settings.AI_SCHEMA_VERSION,
                        settings.OPENAI_MODEL,
                        artifact,
                        tokens_prompt,
                        tokens_completion,
                        cost_usd,
                    )

                    insights[section.id] = artifact

                    if len(insights) == 1:
                        key_manager.record_success(key_id)

                    break  # Success, exit retry loop

                except ValidationError as e:
                    # Pydantic validation failed - AI returned invalid JSON structure
                    logger.error(
                        f"JSON validation failed for section {section.id}: {e.errors()}"
                    )
                    logger.error(
                        f"AI response snippet (first 300 chars): {json_str[:300] if 'json_str' in locals() else 'N/A'}"
                    )
                    key_manager.record_failure(key_id, e)
                    insights[section.id] = create_degraded_artifact(section.id)
                    break  # Don't retry validation errors

                except AuthenticationError as e:
                    logger.error(
                        f"Authentication failed for section {section.id} with key {key_id}: {e}"
                    )
                    key_manager.record_failure(key_id, e)

                    if attempt < max_retries and not retry_attempted:
                        try:
                            key_id, api_key = key_manager.get_next_key()
                            client = OpenAI(
                                api_key=api_key, timeout=settings.OPENAI_TIMEOUT
                            )
                            logger.info(
                                f"Retrying section {section.id} with next API key {key_id}"
                            )
                            retry_attempted = True
                            continue  # Retry with new key
                        except ValueError:
                            logger.error("No more API keys available for retry")
                            insights[section.id] = create_degraded_artifact(section.id)
                            break
                    else:
                        insights[section.id] = create_degraded_artifact(section.id)
                        break

                except RateLimitError as e:
                    logger.error(
                        f"Rate limit exceeded for section {section.id} with key {key_id}: {e}"
                    )
                    key_manager.record_failure(key_id, e)

                    if attempt < max_retries and not retry_attempted:
                        try:
                            key_id, api_key = key_manager.get_next_key()
                            client = OpenAI(
                                api_key=api_key, timeout=settings.OPENAI_TIMEOUT
                            )
                            logger.info(
                                f"Retrying section {section.id} with next API key {key_id} after rate limit"
                            )
                            retry_attempted = True
                            continue  # Retry with new key
                        except ValueError:
                            logger.error("No more API keys available for retry")
                            insights[section.id] = create_degraded_artifact(section.id)
                            break
                    else:
                        insights[section.id] = create_degraded_artifact(section.id)
                        break

                except (APIConnectionError, APIError) as e:
                    logger.error(
                        f"API connection/error for section {section.id} with key {key_id}: {type(e).__name__}: {e}"
                    )
                    key_manager.record_failure(key_id, e)

                    if attempt < max_retries and not retry_attempted:
                        try:
                            key_id, api_key = key_manager.get_next_key()
                            client = OpenAI(
                                api_key=api_key, timeout=settings.OPENAI_TIMEOUT
                            )
                            logger.info(
                                f"Retrying section {section.id} with next API key {key_id} after API error"
                            )
                            retry_attempted = True
                            continue  # Retry with new key
                        except ValueError:
                            logger.error("No more API keys available for retry")
                            insights[section.id] = create_degraded_artifact(section.id)
                            break
                    else:
                        insights[section.id] = create_degraded_artifact(section.id)
                        break

                except SQLAlchemyError as e:
                    logger.error(
                        f"Database error for section {section.id}: {type(e).__name__}: {e}"
                    )
                    key_manager.record_failure(key_id, e)
                    insights[section.id] = create_degraded_artifact(section.id)
                    break  # Don't retry DB errors

                except OpenAIError as e:
                    logger.error(
                        f"OpenAI error for section {section.id} with key {key_id}: {type(e).__name__}: {e}"
                    )
                    key_manager.record_failure(key_id, e)
                    insights[section.id] = create_degraded_artifact(section.id)
                    break  # Don't retry other OpenAI errors

                except Exception as e:
                    logger.exception(
                        f"Unexpected error generating AI insight for section {section.id} with key {key_id}: {e}"
                    )
                    key_manager.record_failure(key_id, e)
                    insights[section.id] = create_degraded_artifact(section.id)
                    break  # Don't retry unexpected errors

    if total_redactions > 0:
        security_metrics.increment_pii_redactions(total_redactions)
        logger.info(f"Total PII redactions in report: {total_redactions}")

    return insights


def safe_validate_section_artifact(json_str: str, section_id: str) -> SectionAIArtifact:
    """Validate and clamp fields to prevent validation errors

    This ensures a single overlong field doesn't degrade the entire section.
    """
    import json

    try:
        data = json.loads(json_str)

        if "gaps" in data and isinstance(data["gaps"], list):
            for gap in data["gaps"]:
                if "gap" in gap and isinstance(gap["gap"], str):
                    if len(gap["gap"]) > 900:
                        original_length = len(gap["gap"])
                        gap["gap"] = gap["gap"][:897] + "..."
                        logger.warning(
                            f"Section {section_id}: Clamped gap description from "
                            f"{original_length} to 900 chars"
                        )

        if "recommendations" in data and isinstance(data["recommendations"], list):
            for rec in data["recommendations"]:
                if "action" in rec and isinstance(rec["action"], str):
                    if len(rec["action"]) > 450:
                        original_length = len(rec["action"])
                        rec["action"] = rec["action"][:447] + "..."
                        logger.warning(
                            f"Section {section_id}: Clamped recommendation action from "
                            f"{original_length} to 450 chars"
                        )

        return SectionAIArtifact.model_validate(data)

    except json.JSONDecodeError as e:
        logger.error(f"Section {section_id}: Invalid JSON from OpenAI: {e}")
        raise ValidationError(f"Invalid JSON: {e}")
    except ValidationError:
        raise


async def generate_ai_insights_async(
    responses: list[AssessmentResponse],
    structure: Any,
    key_manager: OpenAIKeyManager,
    report_id: str,
    max_concurrent: int | None = None,
) -> dict[str, SectionAIArtifact]:
    """Generate AI insights for each section with parallel processing"""

    if max_concurrent is None:
        max_concurrent = settings.AI_MAX_CONCURRENT_SECTIONS

    insights = {}
    response_dict = {r.question_id: r for r in responses}
    cache_service = AICacheService()
    semaphore = asyncio.Semaphore(max_concurrent)

    extractor = get_enhanced_context_extractor()
    pii_redactor = PIIRedactor() if settings.ENABLE_PII_REDACTION_BEFORE_AI else None

    async def process_section(
        section: Any,
    ) -> tuple[Any, SectionAIArtifact, bool] | None:
        """Process a single section with rate limiting"""
        db = SessionLocal()
        section_redactions = 0
        try:
            async with semaphore:
                section_responses = []
                for question in section.questions:
                    response = response_dict.get(question.id)
                    if response:
                        answer_value = response.answer_value
                        comment_value = response.comment if response.comment else None

                        if pii_redactor:
                            answer_str = str(answer_value) if answer_value else ""
                            redacted_answer_str, answer_redaction_count = (
                                pii_redactor.redact(answer_str)
                            )
                            if answer_redaction_count > 0:
                                section_redactions += answer_redaction_count
                                logger.info(
                                    f"PII redacted in answer for question {question.id} (async, {answer_redaction_count} items)"
                                )
                            answer_value = redacted_answer_str  # type: ignore[assignment]

                            if comment_value:
                                redacted_comment, comment_redaction_count = (
                                    pii_redactor.redact(str(comment_value))
                                )
                                if comment_redaction_count > 0:
                                    section_redactions += comment_redaction_count
                                    logger.info(
                                        f"PII redacted in comment for question {question.id} (async, {comment_redaction_count} items)"
                                    )
                                comment_value = redacted_comment  # type: ignore[assignment]

                        resp_dict = {
                            "question": question.text,
                            "answer": answer_value,
                            "weight": question.weight,
                        }

                        if settings.INCLUDE_COMMENTS_IN_AI and comment_value:
                            resp_dict["comment"] = comment_value

                        if settings.INCLUDE_ENHANCED_CONTEXT_IN_AI:
                            context = extractor.get_compact_context(
                                question.id,
                                str(response.answer_value),
                                max_chars=settings.MAX_CONTEXT_CHARS,
                                question_options=question.options,
                            )
                            if context:
                                if pii_redactor:
                                    redacted_context, context_redaction_count = (
                                        pii_redactor.redact(context)
                                    )
                                    if context_redaction_count > 0:
                                        section_redactions += context_redaction_count
                                        logger.info(
                                            f"PII redacted in context for question {question.id} (async, {context_redaction_count} items)"
                                        )
                                    context = redacted_context
                                resp_dict["context"] = context

                        section_responses.append(resp_dict)

                if not section_responses:
                    return None

                answers_hash = cache_service.compute_answers_hash(section_responses)
                cached_artifact = cache_service.get_cached_artifact(
                    db,
                    section.id,
                    answers_hash,
                    settings.AI_PROMPT_VERSION,
                    settings.OPENAI_MODEL,
                )

                if cached_artifact:
                    logger.info(f"Cache HIT for section {section.id}")
                    db_artifact = AISectionArtifactModel(
                        report_id=report_id,
                        section_id=section.id,
                        artifact_json=cached_artifact.model_dump(),
                    )
                    db.add(db_artifact)
                    db.commit()
                    return (section.id, cached_artifact, False)

                logger.info(f"Cache MISS for section {section.id} - calling OpenAI")

                await asyncio.sleep(random.uniform(0, 0.5))

                for attempt in range(settings.AI_MAX_RETRIES):
                    try:
                        key_id, api_key = key_manager.get_next_key()

                        client = AsyncOpenAI(
                            api_key=api_key, timeout=settings.OPENAI_TIMEOUT
                        )

                        curated_context = (
                            benchmark_context_service.get_relevant_context(
                                section.title, section.description, max_controls=5
                            )
                        )
                        prompt, redaction_count = build_section_prompt_v2(
                            section, section_responses, curated_context
                        )

                        start_time = time.time()
                        response = await client.chat.completions.create(  # type: ignore[assignment]
                            model=settings.OPENAI_MODEL,
                            messages=[{"role": "user", "content": prompt}],
                            response_format={"type": "json_object"},
                            temperature=settings.OPENAI_TEMPERATURE,
                            **get_token_params(settings.OPENAI_MAX_TOKENS),
                        )
                        latency_ms = int((time.time() - start_time) * 1000)

                        if not response or not response.choices:
                            raise ValueError("Empty response from OpenAI")

                        json_str = response.choices[0].message.content
                        artifact = safe_validate_section_artifact(json_str, section.id)

                        db_artifact = AISectionArtifactModel(
                            report_id=report_id,
                            section_id=section.id,
                            artifact_json=artifact.model_dump(),
                        )
                        db.add(db_artifact)

                        tokens_prompt = (
                            response.usage.prompt_tokens if response.usage else 0
                        )
                        tokens_completion = (
                            response.usage.completion_tokens if response.usage else 0
                        )
                        finish_reason = (
                            response.choices[0].finish_reason
                            if response.choices
                            else None
                        )
                        cost_usd = (
                            (tokens_prompt * 0.00001 + tokens_completion * 0.00003)
                            if response.usage
                            else 0.0
                        )

                        logger.info(
                            f"Section {section.id}: finish_reason={finish_reason}, "
                            f"tokens={tokens_prompt}+{tokens_completion}={tokens_prompt + tokens_completion}"
                        )

                        metadata = AIGenerationMetadata(
                            report_id=report_id,
                            section_id=section.id,
                            prompt_version=settings.AI_PROMPT_VERSION,
                            schema_version=settings.AI_SCHEMA_VERSION,
                            model=settings.OPENAI_MODEL,
                            temperature=settings.OPENAI_TEMPERATURE,
                            max_tokens=settings.OPENAI_MAX_TOKENS,
                            tokens_prompt=tokens_prompt,
                            tokens_completion=tokens_completion,
                            finish_reason=finish_reason,
                            total_cost_usd=cost_usd,
                            latency_ms=latency_ms,
                        )
                        db.add(metadata)

                        cache_service.store_artifact(
                            db,
                            section.id,
                            answers_hash,
                            settings.AI_PROMPT_VERSION,
                            settings.AI_SCHEMA_VERSION,
                            settings.OPENAI_MODEL,
                            artifact,
                            tokens_prompt,
                            tokens_completion,
                            cost_usd,
                        )

                        db.commit()

                        key_manager.record_success(key_id)

                        logger.info(
                            f"Generated AI insight for section {section.id} ({latency_ms}ms)"
                        )
                        return (section.id, artifact, False)

                    except (RateLimitError, APIConnectionError, APIError) as e:
                        logger.warning(
                            f"Retryable error for section {section.id} (attempt {attempt + 1}/{settings.AI_MAX_RETRIES}): {e}"
                        )
                        key_manager.record_failure(key_id, e)

                        if attempt < settings.AI_MAX_RETRIES - 1:
                            await asyncio.sleep(
                                settings.AI_RETRY_DELAY_SECONDS * (2**attempt)
                            )
                            continue
                        else:
                            if (
                                settings.AI_FALLBACK_MODEL
                                and settings.AI_FALLBACK_MODEL != settings.OPENAI_MODEL
                            ):
                                logger.info(
                                    f"Falling back to {settings.AI_FALLBACK_MODEL} for section {section.id}"
                                )
                                try:
                                    fallback_response = (
                                        await client.chat.completions.create(
                                            model=settings.AI_FALLBACK_MODEL,
                                            messages=[
                                                {"role": "user", "content": prompt}
                                            ],
                                            response_format={"type": "json_object"},
                                            max_tokens=800,  # Shorter for fallback
                                            temperature=0.5,
                                        )
                                    )

                                    json_str = fallback_response.choices[
                                        0
                                    ].message.content
                                    if json_str:
                                        artifact = safe_validate_section_artifact(
                                            json_str, section.id
                                        )
                                    else:
                                        raise ValueError("Empty fallback response")

                                    db_artifact = AISectionArtifactModel(
                                        report_id=report_id,
                                        section_id=section.id,
                                        artifact_json=artifact.model_dump(),
                                    )
                                    db.add(db_artifact)
                                    db.commit()

                                    logger.info(
                                        f"Fallback successful for section {section.id}"
                                    )
                                    return (section.id, artifact, True)  # Degraded
                                except Exception as fallback_error:
                                    logger.error(
                                        f"Fallback also failed for section {section.id}: {fallback_error}"
                                    )

                            logger.error(
                                f"All retries exhausted for section {section.id}"
                            )
                            db.rollback()
                            degraded_artifact = create_degraded_artifact(section.id)
                            return (section.id, degraded_artifact, True)

                    except ValidationError as e:
                        logger.error(
                            f"JSON validation failed for section {section.id}: {e.errors()}"
                        )
                        key_manager.record_failure(key_id, e)
                        db.rollback()
                        degraded_artifact = create_degraded_artifact(section.id)
                        return (section.id, degraded_artifact, True)

                    except Exception as e:
                        logger.exception(
                            f"Unexpected error for section {section.id}: {e}"
                        )
                        key_manager.record_failure(key_id, e)
                        db.rollback()
                        degraded_artifact = create_degraded_artifact(section.id)
                        return (section.id, degraded_artifact, True)
        finally:
            db.close()
        return None

    tasks = [process_section(section) for section in structure.sections]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if result and not isinstance(result, Exception):
            section_id, artifact, is_degraded = result  # type: ignore[misc]
            insights[section_id] = artifact
        elif isinstance(result, Exception):
            error_msg = str(result)
            logger.error(f"Section processing raised exception: {error_msg}")

    return insights


def create_degraded_artifact(section_id: str) -> SectionAIArtifact:
    """Create a degraded artifact when AI generation fails"""
    return SectionAIArtifact(
        schema_version=settings.AI_SCHEMA_VERSION,
        risk_level="Medium",
        risk_explanation="AI analysis temporarily unavailable for this section. Please contact support for manual analysis.",
        strengths=["Assessment data collected successfully"],
        gaps=[
            Gap(
                gap="AI analysis unavailable",
                linked_signals=["Q1"],
                severity="Low",
            )
        ],
        recommendations=[
            Recommendation(
                action="Retry AI analysis or request manual review",
                rationale="Automated analysis encountered an error",
                linked_signals=["Q1"],
                effort="Low",
                impact="Low",
                timeline="30-day",
                references=[],
            )
        ],
        benchmarks=[
            Benchmark(
                control="Assessment Completion",
                status="Implemented",
                framework="Internal",
                reference="",
            )
        ],
        confidence_score=0.0,
    )


def format_responses_for_ai(responses: list[dict]) -> str:
    """Format responses for AI analysis"""

    formatted = []
    for resp in responses:
        formatted.append(f"Q: {resp['question']}")
        formatted.append(f"A: {resp['answer']} (Weight: {resp['weight']})")
        formatted.append("")

    return "\n".join(formatted)


def compute_blind_spots(
    structure: Any, responses: list[AssessmentResponse]
) -> dict[str, Any]:
    """
    Compute blind spots by scanning responses for unknown/not_sure answers.
    Returns dict with summary counts per section and list of blind spot items.
    """
    response_dict = {r.question_id: r for r in responses}
    blind_spots_by_section = {}
    all_blind_spots = []

    unknown_values = [
        "unknown",
        "not_sure",
        "not sure",
        "don't_know",
        "dont_know",
        "don't know",
        "dont know",
    ]

    for section in structure.sections:
        section_blind_spots = []
        for question in section.questions:
            response = response_dict.get(question.id)
            if response:
                mapped_answer = map_numeric_to_slug(
                    question, str(response.answer_value)
                )
                answer_normalized = normalize_option_value(mapped_answer)
                if answer_normalized in unknown_values:
                    blind_spot_item = {
                        "section_id": section.id,
                        "section_title": section.title,
                        "question_id": question.id,
                        "question_text": question.text,
                    }
                    section_blind_spots.append(blind_spot_item)
                    all_blind_spots.append(blind_spot_item)

        if section_blind_spots:
            blind_spots_by_section[section.id] = {
                "count": len(section_blind_spots),
                "items": section_blind_spots[:3],
            }

    return {
        "by_section": blind_spots_by_section,
        "total_count": len(all_blind_spots),
        "all_items": all_blind_spots,
    }


def get_selected_option_explanation(
    question: Question, answer_value: str
) -> dict[str, Any] | None:
    """
    Get detailed explanation for the selected option.
    Returns dict with explanation fields or None if not available.
    """
    if not settings.ENHANCED_REPORT_EXPLANATIONS:
        return None

    mapped_answer = map_numeric_to_slug(question, str(answer_value))

    for option in question.options:
        if str(option.value) == str(mapped_answer):
            if option.detailed_explanation:
                exp = option.detailed_explanation
                return {
                    "definition": exp.definition,
                    "why_matters": exp.why_matters,
                    "recommendation": exp.recommendation,
                    "path_to_improvement": exp.path_to_improvement,
                }
    return None


def generate_report_html(
    assessment: Any,
    responses: list[AssessmentResponse],
    scores: dict[str, Any],
    structure: Any,
) -> str:
    """Generate HTML content for standard report"""

    template = jinja_env.from_string(
        """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Security Posture Assessment Report</title>
        <style>
            body { font-family: 'Aptos (Body)', Arial, sans-serif; font-size: 12px; margin: 0; padding: 40px; line-height: 1.6; color: #333; }
            .container { max-width: 85%; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 40px; border-bottom: 3px solid #2c3e50; padding-bottom: 20px; }
            .section { margin-bottom: 30px; page-break-inside: avoid; }
            .score-box { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }
            .high-score { background: #d4edda; border-left: 4px solid #28a745; }
            .medium-score { background: #fff3cd; border-left: 4px solid #ffc107; }
            .low-score { background: #f8d7da; border-left: 4px solid #dc3545; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 0.9em; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #2c3e50; color: white; font-weight: bold; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .toc { background: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 30px; }
            .toc ul { list-style-type: none; padding-left: 0; }
            .toc li { margin: 8px 0; }
            .toc a { color: #2c3e50; text-decoration: none; }
            .toc a:hover { text-decoration: underline; }
            .metadata-box { background: #e9ecef; padding: 15px; border-radius: 5px; margin: 15px 0; }
            .confidence-box { padding: 10px; border-radius: 5px; margin: 10px 0; font-weight: bold; }
            .heatmap { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; margin: 20px 0; }
            .heatmap-item { padding: 15px; border-radius: 5px; text-align: center; }
            .remediation-table td { vertical-align: top; }
            .priority-p1 { color: #dc3545; font-weight: bold; }
            .priority-p2 { color: #fd7e14; font-weight: bold; }
            .priority-p3 { color: #28a745; font-weight: bold; }
            .question-row { page-break-inside: avoid; }
            .question-text { font-weight: bold; color: #2c3e50; }
            .answer-text { color: #495057; }
            .comment-text { font-style: italic; color: #6c757d; background: #f8f9fa; padding: 5px; border-radius: 3px; }
            .weight-badge { background: #6c757d; color: white; padding: 2px 8px; border-radius: 3px; font-size: 0.85em; }
            h1 { font-family: 'Aptos (Body)', Arial, sans-serif; font-size: 16px; color: #2c3e50; }
            h2 { font-family: 'Aptos (Body)', Arial, sans-serif; font-size: 16px; color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; margin-top: 30px; }
            h3 { font-family: 'Aptos (Body)', Arial, sans-serif; font-size: 14px; color: #495057; margin-top: 20px; }
            .summary-box { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #6c757d; }
            .strength-item { color: #28a745; }
            .gap-item { color: #dc3545; }
        </style>
    </head>
    <body>
        <div class="container">
        <div class="header">
            <h1>Security Posture Assessment Report</h1>
            <p><strong>Generated on:</strong> {{ report_date }}</p>
            <p><strong>Assessment Period:</strong> {{ assessment.started_at.strftime('%Y-%m-%d') }} to {{ assessment.completed_at.strftime('%Y-%m-%d') }}</p>
        </div>
        
        <div class="section toc">
            <h2>Table of Contents</h2>
            <ul>
                <li><a href="#executive-summary">1. Executive Summary</a></li>
                <li><a href="#assessment-overview">2. Assessment Overview and Metadata</a></li>
                <li><a href="#methodology">3. Methodology and Scoring</a></li>
                <li><a href="#data-quality">4. Data Quality and Confidence Level</a></li>
                <li><a href="#domain-heatmap">5. Domain Heatmap and Maturity Tiers</a></li>
                <li><a href="#section-scores">6. Section Scores</a></li>
                <li><a href="#remediation-plan">7. Prioritized Remediation Plan</a></li>
                <li><a href="#section-summaries">8. Section Summaries</a></li>
                <li><a href="#recommendations">9. Overall Recommendations</a></li>
                <li><a href="#detailed-responses">10. Detailed Responses (All Questions and Answers)</a></li>
                <li><a href="#comments-digest">11. Comments Digest</a></li>
                {% if assessment.consultation_interest %}
                <li><a href="#consultation">12. Consultation Request</a></li>
                {% endif %}
                <li><a href="#disclaimer">Disclaimer</a></li>
            </ul>
        </div>
        
        <div class="section" id="executive-summary">
            <h2>1. Executive Summary</h2>
            <div class="score-box {{ overall_score_class }}">
                <h3>Overall Security Score: {{ "%.1f"|format(scores.overall.percentage) }}%</h3>
                <p>{{ overall_assessment }}</p>
            </div>
        </div>
        
        <div class="section" id="assessment-overview">
            <h2>2. Assessment Overview and Metadata</h2>
            <div class="metadata-box">
                <p><strong>Assessment ID:</strong> {{ assessment.id }}</p>
                <p><strong>Started:</strong> {{ assessment.started_at.strftime('%Y-%m-%d %H:%M UTC') }}</p>
                <p><strong>Completed:</strong> {{ assessment.completed_at.strftime('%Y-%m-%d %H:%M UTC') }}</p>
                <p><strong>Total Questions:</strong> {{ structure.total_questions }}</p>
                <p><strong>Questions Answered:</strong> {{ responses|length }}</p>
                <p><strong>Overall Progress:</strong> {{ "%.1f"|format(assessment.progress_percentage) }}%</p>
                <p><strong>Report Version:</strong> Standard Report v1.0</p>
            </div>
            <p>This assessment evaluates your organization's cybersecurity posture across {{ structure.sections|length }} key security domains. 
            The evaluation is based on industry best practices and provides actionable insights for improving your security program.</p>
        </div>
        
        <div class="section" id="methodology">
            <h2>3. Methodology and Scoring</h2>
            <p>This assessment uses a weighted scoring methodology to evaluate your security posture:</p>
            <ul>
                <li><strong>Question Types:</strong>
                    <ul>
                        <li><em>Yes/No Questions:</em> Full weight awarded for "Yes" answers, zero for "No"</li>
                        <li><em>Multiple Choice:</em> Weight awarded for selecting an answer</li>
                        <li><em>Multiple Select:</em> Weight awarded for selecting one or more answers</li>
                        <li><em>Text Questions:</em> Not scored, used for context and planning</li>
                    </ul>
                </li>
                <li><strong>Question Weights:</strong> Questions are weighted 1-5 based on their importance to security posture</li>
                <li><strong>Section Scores:</strong> Calculated as (total points earned / total possible points) × 100%</li>
                <li><strong>Overall Score:</strong> Aggregate of all section scores weighted equally</li>
                <li><strong>Maturity Tiers:</strong>
                    <ul>
                        <li><em>Strong (≥80%):</em> Robust security practices in place</li>
                        <li><em>Moderate (60-79%):</em> Foundational practices with room for improvement</li>
                        <li><em>Needs Improvement (<60%):</em> Significant gaps requiring attention</li>
                    </ul>
                </li>
            </ul>
        </div>
        
        <div class="section" id="data-quality">
            <h2>4. Data Quality and Confidence Level</h2>
            <div class="confidence-box {{ confidence_class }}">
                <p><strong>Confidence Level:</strong> {{ confidence_level }}</p>
                <p>{{ confidence_description }}</p>
            </div>
            <table>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Total Questions</td>
                    <td>{{ structure.total_questions }}</td>
                </tr>
                <tr>
                    <td>Questions Answered</td>
                    <td>{{ responses|length }}</td>
                </tr>
                <tr>
                    <td>Questions Unanswered</td>
                    <td>{{ structure.total_questions - responses|length }}</td>
                </tr>
                <tr>
                    <td>Overall Completion Rate</td>
                    <td>{{ "%.1f"|format(assessment.progress_percentage) }}%</td>
                </tr>
                <tr>
                    <td>Comments Provided</td>
                    <td>{{ comments_count }}</td>
                </tr>
                {% if enhanced_explanations_enabled and blind_spots.total_count > 0 %}
                <tr>
                    <td>Blind Spots (Unknown/Not Sure)</td>
                    <td>{{ blind_spots.total_count }}</td>
                </tr>
                {% endif %}
            </table>
            
            {% if enhanced_explanations_enabled and blind_spots.total_count > 0 %}
            <div class="summary-box" style="border-left: 4px solid #ffc107; background: #fff3cd;">
                <h3>⚠️ Knowledge Gaps Identified</h3>
                <p>You indicated "Not sure" or "Unknown" for {{ blind_spots.total_count }} question(s). These represent blind spots in your security posture that warrant investigation:</p>
                <table>
                    <tr>
                        <th>Section</th>
                        <th>Unknown Count</th>
                    </tr>
                    {% for section_id, section_data in blind_spots.by_section.items() %}
                    <tr>
                        <td>{{ section_data.items[0].section_title }}</td>
                        <td>{{ section_data.count }}</td>
                    </tr>
                    {% endfor %}
                </table>
                <p><strong>Recommendation:</strong> These blind spots represent areas where you lack visibility or knowledge. Prioritize investigating these areas to understand your actual security posture and identify potential risks.</p>
            </div>
            {% endif %}
        </div>
        
        <div class="section" id="domain-heatmap">
            <h2>5. Domain Heatmap and Maturity Tiers</h2>
            <p>Visual overview of security maturity across all domains:</p>
            <div class="heatmap">
                {% for section in structure.sections %}
                <div class="heatmap-item {{ maturity_tiers[section.id].css_class }}">
                    <strong>{{ section.title }}</strong><br>
                    {{ "%.1f"|format(scores[section.id].percentage) }}%<br>
                    <small>{{ maturity_tiers[section.id].tier }}</small>
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="section" id="section-scores">
            <h2>6. Section Scores</h2>
            <table>
                <tr>
                    <th>Section</th>
                    <th>Score</th>
                    <th>Completion</th>
                    <th>Maturity Tier</th>
                </tr>
                {% for section in structure.sections %}
                <tr>
                    <td>{{ section.title }}</td>
                    <td>{{ "%.1f"|format(scores[section.id].percentage) }}%</td>
                    <td>{{ "%.1f"|format(scores[section.id].completion_rate) }}%</td>
                    <td>{{ maturity_tiers[section.id].tier }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        
        <div class="section" id="remediation-plan">
            <h2>7. Prioritized Remediation Plan</h2>
            <p>Recommended actions prioritized by impact and urgency:</p>
            {% if remediation_items %}
            <table class="remediation-table">
                <tr>
                    <th>Priority</th>
                    <th>Domain</th>
                    <th>Current Score</th>
                    <th>Effort</th>
                    <th>Timeframe</th>
                </tr>
                {% for item in remediation_items %}
                <tr>
                    <td class="priority-{{ item.priority|lower }}">{{ item.priority }}</td>
                    <td>{{ item.domain }}</td>
                    <td>{{ item.current_score }}</td>
                    <td>{{ item.effort }}</td>
                    <td>{{ item.timeframe }}</td>
                </tr>
                {% endfor %}
            </table>
            <p><strong>Priority Levels:</strong></p>
            <ul>
                <li><span class="priority-p1">P1 (Critical):</span> Address immediately - significant security gaps</li>
                <li><span class="priority-p2">P2 (High):</span> Address within 30-90 days - important improvements</li>
                <li><span class="priority-p3">P3 (Medium):</span> Quick wins - low effort, visible improvements</li>
            </ul>
            {% else %}
            <p>No critical remediation items identified. Continue maintaining current security practices.</p>
            {% endif %}
        </div>
        
        <div class="section" id="section-summaries">
            <h2>8. Section Summaries</h2>
            <p>Detailed analysis of each security domain:</p>
            {% for summary in section_summaries %}
            <div class="summary-box">
                <h3>{{ summary.section.title }}</h3>
                <p><strong>Score:</strong> {{ "%.1f"|format(summary.score) }}% | 
                   <strong>Completion:</strong> {{ "%.1f"|format(summary.completion) }}%</p>
                
                {% if summary.strengths %}
                <p><strong>Key Strengths:</strong></p>
                <ul>
                    {% for strength in summary.strengths %}
                    <li class="strength-item">{{ strength }}</li>
                    {% endfor %}
                </ul>
                {% endif %}
                
                {% if summary.gaps %}
                <p><strong>Critical Gaps:</strong></p>
                <ul>
                    {% for gap in summary.gaps %}
                    <li class="gap-item">{{ gap }}</li>
                    {% endfor %}
                </ul>
                {% endif %}
                
                {% if summary.recommendations %}
                <p><strong>Recommendations:</strong></p>
                <ul>
                    {% for rec in summary.recommendations %}
                    <li>{{ rec }}</li>
                    {% endfor %}
                </ul>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        
        <div class="section" id="recommendations">
            <h2>9. Overall Recommendations</h2>
            <ul>
                {% for recommendation in recommendations %}
                <li>{{ recommendation }}</li>
                {% endfor %}
            </ul>
        </div>
        
        <div class="section" id="detailed-responses">
            <h2>10. Detailed Responses (All Questions and Answers)</h2>
            <p>Complete record of all assessment questions with your submitted answers and comments:</p>
            {% for section in structure.sections %}
            <div class="section">
                <h3>{{ section.title }}</h3>
                <table>
                    <tr>
                        <th style="width: 50%;">Question</th>
                        <th style="width: 25%;">Answer</th>
                        <th style="width: 15%;">Comment</th>
                        <th style="width: 10%;">Weight</th>
                    </tr>
                    {% for question in section.questions %}
                    <tr class="question-row">
                        <td class="question-text">{{ question.text }}</td>
                        <td class="answer-text">{{ question_answers[question.id] }}</td>
                        <td class="comment-text">{{ question_comments[question.id] }}</td>
                        <td><span class="weight-badge">{{ question.weight }}</span></td>
                    </tr>
                    {% if enhanced_explanations_enabled and question_explanations[question.id] %}
                    <tr class="question-row">
                        <td colspan="4" style="background: #f8f9fa; padding: 10px; font-size: 0.9em;">
                            {% set exp = question_explanations[question.id] %}
                            {% if exp.definition %}
                            <p><strong>What this means:</strong> {{ exp.definition[:500] }}{% if exp.definition|length > 500 %}...{% endif %}</p>
                            {% endif %}
                            {% if exp.recommendation %}
                            <p><strong>Recommendation:</strong> {{ exp.recommendation[:500] }}{% if exp.recommendation|length > 500 %}...{% endif %}</p>
                            {% endif %}
                        </td>
                    </tr>
                    {% endif %}
                    {% endfor %}
                </table>
            </div>
            {% endfor %}
        </div>
        
        <div class="section" id="comments-digest">
            <h2>11. Comments Digest</h2>
            <p>All comments provided during the assessment, grouped by domain:</p>
            {% if all_comments %}
            {% for section in structure.sections %}
                {% if section_comments[section.id] %}
                <div class="summary-box">
                    <h3>{{ section.title }}</h3>
                    {% for comment_item in section_comments[section.id] %}
                    <p><strong>Q:</strong> {{ comment_item.question }}<br>
                       <strong>Comment:</strong> <em>{{ comment_item.comment }}</em></p>
                    {% endfor %}
                </div>
                {% endif %}
            {% endfor %}
            {% else %}
            <p>No comments were provided during this assessment.</p>
            {% endif %}
        </div>
        
        {% if assessment.consultation_interest %}
        <div class="section" id="consultation">
            <h2>12. Consultation Request</h2>
            <div class="score-box medium-score">
                <p><strong>Consultation Interest:</strong> Yes</p>
                {% if assessment.consultation_details %}
                <p><strong>Details:</strong></p>
                <p>{{ assessment.consultation_details }}</p>
                {% endif %}
                <p><em>An EchoStor security consultant will contact you to discuss your specific needs and how we can help improve your security posture.</em></p>
            </div>
        </div>
        {% endif %}
        
        <div class="section" id="disclaimer">
            <h2>Disclaimer</h2>
            <p>This assessment provides general guidance based on industry best practices and your self-reported responses. 
            The scores and recommendations are indicative and should be validated through comprehensive security audits. 
            For detailed security architecture planning, penetration testing, or compliance assessments, 
            please contact EchoStor's security team for a professional evaluation tailored to your organization's specific needs.</p>
        </div>
        </div>
    </body>
    </html>
    """
    )

    overall_percentage = scores["overall"]["percentage"]
    if overall_percentage >= 80:
        overall_score_class = "high-score"
        overall_assessment = (
            "Strong security posture with good coverage across most areas."
        )
    elif overall_percentage >= 60:
        overall_score_class = "medium-score"
        overall_assessment = (
            "Moderate security posture with room for improvement in several areas."
        )
    else:
        overall_score_class = "low-score"
        overall_assessment = (
            "Security posture needs significant improvement across multiple areas."
        )

    recommendations = generate_recommendations(scores, structure)

    confidence_level, confidence_description = calculate_confidence_level(scores)
    if confidence_level == "High":
        confidence_class = "high-score"
    elif confidence_level == "Medium":
        confidence_class = "medium-score"
    else:
        confidence_class = "low-score"

    maturity_tiers = {}
    for section in structure.sections:
        tier, css_class = get_maturity_tier(scores[section.id]["percentage"])
        maturity_tiers[section.id] = {"tier": tier, "css_class": css_class}

    remediation_items = generate_prioritized_remediation(scores, structure)
    section_summaries = generate_section_summaries(scores, structure, responses)

    blind_spots = compute_blind_spots(structure, responses)

    response_dict = {r.question_id: r for r in responses}
    question_answers = {}
    question_comments = {}
    question_explanations = {}

    for section in structure.sections:
        for question in section.questions:
            response = response_dict.get(question.id)
            if response:
                question_answers[question.id] = normalize_answer_display(
                    response.answer_value, question
                )
                question_comments[question.id] = (
                    response.comment if response.comment else "—"
                )
                question_explanations[question.id] = get_selected_option_explanation(
                    question, str(response.answer_value)
                )
            else:
                question_answers[question.id] = "Not answered"
                question_comments[question.id] = "—"
                question_explanations[question.id] = None

    all_comments = []
    section_comments: dict[str, list] = {}
    comments_count = 0

    for section in structure.sections:
        section_comments[section.id] = []
        for question in section.questions:
            response = response_dict.get(question.id)
            if response and response.comment:
                comments_count += 1
                all_comments.append(
                    {
                        "section": section.title,
                        "question": question.text,
                        "comment": response.comment,
                    }
                )
                section_comments[section.id].append(
                    {"question": question.text, "comment": response.comment}
                )

    return template.render(
        assessment=assessment,
        scores=scores,
        structure=structure,
        responses=responses,
        report_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        overall_score_class=overall_score_class,
        overall_assessment=overall_assessment,
        recommendations=recommendations,
        confidence_level=confidence_level,
        confidence_description=confidence_description,
        confidence_class=confidence_class,
        maturity_tiers=maturity_tiers,
        remediation_items=remediation_items,
        section_summaries=section_summaries,
        question_answers=question_answers,
        question_comments=question_comments,
        question_explanations=question_explanations,
        all_comments=all_comments,
        section_comments=section_comments,
        comments_count=comments_count,
        blind_spots=blind_spots,
        enhanced_explanations_enabled=settings.ENHANCED_REPORT_EXPLANATIONS,
    )


def generate_ai_report_html(
    assessment: Any,
    responses: list[AssessmentResponse],
    scores: dict[str, Any],
    structure: Any,
    ai_insights: dict[str, SectionAIArtifact],
    synthesis: SynthesisArtifact | None = None,
) -> str:
    """Generate HTML content for AI-enhanced report with synthesis"""

    jinja_env.filters["markdown"] = markdown_filter

    template = jinja_env.from_string(
        """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>AI-Enhanced Security Posture Assessment Report</title>
        <style>
            @page {
                margin: 2cm;
                @top-right {
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 10px;
                    color: #666;
                }
                @top-left {
                    content: "AI-Enhanced Security Assessment";
                    font-size: 10px;
                    color: #666;
                }
                @bottom-center {
                    content: "Confidential - {{ report_date }}";
                    font-size: 10px;
                    color: #666;
                }
            }
            body { font-family: 'Aptos (Body)', Arial, sans-serif; font-size: 11px; margin: 0; padding: 0; line-height: 1.6; color: #333; }
            .container { max-width: 100%; margin: 0 auto; }
            .header { text-align: center; margin-bottom: 30px; border-bottom: 3px solid #2c3e50; padding-bottom: 20px; }
            .section { margin-bottom: 25px; page-break-inside: avoid; }
            .score-box { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }
            .ai-insight { background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin: 15px 0; font-size: 10px; }
            .ai-insight h4 { margin-top: 0; color: #2196f3; }
            .ai-insight strong { color: #1976d2; }
            .ai-insight ul, .ai-insight ol { margin: 8px 0; padding-left: 20px; }
            .ai-insight li { margin: 4px 0; }
            .high-score { background: #d4edda; border-left: 4px solid #28a745; }
            .medium-score { background: #fff3cd; border-left: 4px solid #ffc107; }
            .low-score { background: #f8d7da; border-left: 4px solid #dc3545; }
            table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 10px; page-break-inside: avoid; }
            th, td { border: 1px solid #ddd; padding: 10px; text-align: left; vertical-align: top; }
            th { background-color: #2c3e50; color: white; font-weight: bold; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .toc { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; page-break-after: always; }
            .toc h2 { margin-top: 0; }
            .toc ul { list-style-type: none; padding-left: 0; }
            .toc li { margin: 8px 0; padding-left: 20px; }
            .toc a { color: #2c3e50; text-decoration: none; }
            .scorecard-table { margin: 20px 0; }
            .scorecard-table th { background-color: #2c3e50; }
            .methodology-box { background: #f8f9fa; padding: 15px; border-left: 4px solid #6c757d; margin: 15px 0; }
            .priority-p1 { color: #dc3545; font-weight: bold; }
            .priority-p2 { color: #fd7e14; font-weight: bold; }
            .priority-p3 { color: #ffc107; font-weight: bold; }
            .roadmap-table td { vertical-align: top; }
            h1 { font-family: 'Aptos (Body)', Arial, sans-serif; font-size: 18px; color: #2c3e50; margin: 0; }
            h2 { font-family: 'Aptos (Body)', Arial, sans-serif; font-size: 15px; color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 8px; margin-top: 25px; page-break-after: avoid; }
            h3 { font-family: 'Aptos (Body)', Arial, sans-serif; font-size: 13px; color: #495057; margin-top: 15px; page-break-after: avoid; }
            h4 { font-family: 'Aptos (Body)', Arial, sans-serif; font-size: 11px; color: #2196f3; font-weight: bold; margin: 10px 0 5px 0; }
            .page-break { page-break-before: always; }
        </style>
    </head>
    <body>
        <div class="container">
        <!-- Title Page -->
        <div class="header">
            <h1>AI-Enhanced Security Posture Assessment Report</h1>
            <p style="font-size: 12px; margin: 10px 0;">Generated on: {{ report_date }}</p>
            <p>Assessment Period: {{ assessment.started_at.strftime('%Y-%m-%d') }} to {{ assessment.completed_at.strftime('%Y-%m-%d') }}</p>
            <p><em>Enhanced with AI-powered analysis and recommendations</em></p>
        </div>
        
        <!-- Executive Summary -->
        <div class="section">
            <h2 id="executive-summary">Executive Summary</h2>
            <div class="score-box {{ overall_score_class }}">
                <h3>Overall Security Score: {{ "%.1f"|format(scores.overall.percentage) }}%</h3>
                <p>{{ overall_assessment }}</p>
            </div>
            
            {% if synthesis %}
            <div class="ai-insight" style="margin-top: 20px;">
                <h4>🎯 Strategic Overview</h4>
                <p><strong>Overall Risk Level: {{ synthesis.overall_risk_level }}</strong></p>
                <p>{{ synthesis.overall_risk_explanation }}</p>
                
                <div style="margin-top: 15px;">
                    {{ synthesis.executive_summary | markdown | safe }}
                </div>
            </div>
            
            {% if synthesis.cross_cutting_themes %}
            <div class="section" style="margin-top: 20px;">
                <h3>Cross-Cutting Themes</h3>
                <p>The following themes span multiple security domains and require coordinated attention:</p>
                {% for theme in synthesis.cross_cutting_themes %}
                <div class="ai-insight" style="margin: 10px 0;">
                    <h4>{{ theme.theme }} <span style="color: {% if theme.severity == 'Critical' %}#dc3545{% elif theme.severity == 'High' %}#fd7e14{% elif theme.severity == 'Medium' %}#ffc107{% else %}#28a745{% endif %};">({{ theme.severity }})</span></h4>
                    <p>{{ theme.description }}</p>
                    <p><em>Affected domains: {{ theme.affected_domains|join(', ') }}</em></p>
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            {% if synthesis.top_10_initiatives %}
            <div class="section" style="margin-top: 20px;">
                <h3>Top Priority Initiatives</h3>
                <p>The following initiatives are prioritized by impact, urgency, and effort. Dependencies are mapped to ensure proper sequencing.</p>
                <table style="font-size: 9px;">
                    <thead>
                        <tr>
                            <th style="width: 5%;">Priority</th>
                            <th style="width: 25%;">Initiative</th>
                            <th style="width: 15%;">Domains</th>
                            <th style="width: 10%;">Effort</th>
                            <th style="width: 10%;">Impact</th>
                            <th style="width: 10%;">Timeline</th>
                            <th style="width: 25%;">Success Metrics</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for initiative in synthesis.top_10_initiatives[:10] %}
                        <tr>
                            <td class="priority-p{{ (initiative.priority - 1) // 3 + 1 }}" style="text-align: center; font-weight: bold;">{{ initiative.priority }}</td>
                            <td>
                                <strong>{{ initiative.title }}</strong><br>
                                <span style="font-size: 8px;">{{ initiative.description }}</span>
                                {% if initiative.dependencies %}
                                <br><em style="font-size: 8px; color: #666;">Depends on: #{{ initiative.dependencies|join(', #') }}</em>
                                {% endif %}
                            </td>
                            <td style="font-size: 8px;">{{ initiative.affected_domains|join(', ') }}</td>
                            <td>{{ initiative.effort }}</td>
                            <td style="color: {% if initiative.impact == 'Critical' %}#dc3545{% elif initiative.impact == 'High' %}#fd7e14{% else %}#ffc107{% endif %}; font-weight: bold;">{{ initiative.impact }}</td>
                            <td>{{ initiative.timeline }}</td>
                            <td style="font-size: 8px;">
                                <ul style="margin: 0; padding-left: 15px;">
                                    {% for metric in initiative.success_metrics %}
                                    <li>{{ metric }}</li>
                                    {% endfor %}
                                </ul>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            {% endif %}
            
            {% if synthesis.quick_wins %}
            <div class="section" style="margin-top: 20px;">
                <h3>Quick Wins (30-Day Actions)</h3>
                <p>These low-effort, high-impact actions can be completed quickly to demonstrate progress:</p>
                <ul>
                    {% for win in synthesis.quick_wins %}
                    <li>{{ win }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
            
            {% if synthesis.long_term_strategy %}
            <div class="section" style="margin-top: 20px;">
                <h3>Long-Term Strategy (6-12 Months)</h3>
                <div class="methodology-box">
                    <p>{{ synthesis.long_term_strategy }}</p>
                </div>
            </div>
            {% endif %}
            {% endif %}
        </div>
        
        <!-- Table of Contents -->
        <div class="toc">
            <h2>Table of Contents</h2>
            <ul>
                <li>1. <a href="#executive-summary">Executive Summary</a></li>
                <li>2. <a href="#scorecard">Security Scorecard</a></li>
                <li>3. <a href="#methodology">Methodology & Scoring</a></li>
                <li>4. <a href="#section-analysis">Section Analysis with AI Insights</a></li>
                <li>5. <a href="#recommendations">Prioritized Recommendations Roadmap</a></li>
                <li>6. <a href="#disclaimer">Disclaimer & AI Transparency</a></li>
            </ul>
        </div>
        
        <!-- Security Scorecard -->
        <div class="section page-break">
            <h2 id="scorecard">Security Scorecard</h2>
            <p>This scorecard provides an at-a-glance view of your organization's security posture across all assessed domains.</p>
            <table class="scorecard-table">
                <thead>
                    <tr>
                        <th>Domain</th>
                        <th>Score</th>
                        <th>Completion</th>
                        <th>Maturity Level</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for section in structure.sections %}
                    <tr>
                        <td><strong>{{ section.title }}</strong></td>
                        <td>{{ "%.1f"|format(scores[section.id].percentage) }}%</td>
                        <td>{{ scores[section.id].responses_count }}/{{ scores[section.id].total_questions }} questions</td>
                        <td>{{ get_maturity_level(scores[section.id].percentage) }}</td>
                        <td>
                            {% if scores[section.id].percentage >= 80 %}
                            <span style="color: #28a745;">●</span> Strong
                            {% elif scores[section.id].percentage >= 60 %}
                            <span style="color: #ffc107;">●</span> Moderate
                            {% else %}
                            <span style="color: #dc3545;">●</span> Needs Improvement
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                    <tr style="background-color: #e9ecef; font-weight: bold;">
                        <td>OVERALL</td>
                        <td>{{ "%.1f"|format(scores.overall.percentage) }}%</td>
                        <td colspan="3">{{ overall_assessment }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <!-- Methodology -->
        <div class="section">
            <h2 id="methodology">Methodology & Scoring</h2>
            <div class="methodology-box">
                <h3>Assessment Approach</h3>
                <p>This security posture assessment evaluates your organization across multiple cybersecurity domains using a comprehensive questionnaire. Each question is weighted based on its importance to overall security posture.</p>
                
                <h3>Scoring Formula</h3>
                <p><strong>Section Score</strong> = (Sum of weighted correct answers) / (Total possible weighted score) × 100%</p>
                <p><strong>Overall Score</strong> = Average of all section scores weighted by section importance</p>
                
                <h3>Maturity Levels</h3>
                <ul>
                    <li><strong>Strong (80-100%):</strong> Best-in-class security practices with comprehensive controls</li>
                    <li><strong>Moderate (60-79%):</strong> Foundational security in place with room for improvement</li>
                    <li><strong>Developing (40-59%):</strong> Basic security measures with significant gaps</li>
                    <li><strong>Needs Improvement (&lt;40%):</strong> Critical security gaps requiring immediate attention</li>
                </ul>
                
                <h3>AI Analysis</h3>
                <p><strong>AI Model:</strong> {{ ai_model }}</p>
                <p><strong>Analysis Approach:</strong> AI-powered insights are generated by analyzing your responses against industry best practices, security frameworks (NIST, ISO/IEC, OWASP), and peer benchmarks. Each section receives structured analysis covering risk assessment, strengths, gaps, and prioritized recommendations.</p>
                <p><strong>Human Review:</strong> AI analysis is provided for informational purposes and should be validated by qualified security professionals for comprehensive security planning.</p>
            </div>
        </div>
        
        <!-- Section Analysis with AI Insights -->
        <div class="section page-break">
            <h2 id="section-analysis">Section Analysis with AI Insights</h2>
            {% for section in structure.sections %}
            <div class="section">
                <h3>{{ section.title }}</h3>
                <div class="score-box">
                    <strong>Score: {{ "%.1f"|format(scores[section.id].percentage) }}%</strong>
                    ({{ scores[section.id].responses_count }}/{{ scores[section.id].total_questions }} questions completed)
                </div>
                {% if ai_insights.get(section.id) %}
                <div class="ai-insight">
                    <h4>🤖 AI Analysis</h4>
                    {% set artifact = ai_insights[section.id] %}
                    
                    <p><strong>Risk Level: {{ artifact.risk_level }}</strong></p>
                    <p>{{ artifact.risk_explanation }}</p>
                    
                    <h4>Key Strengths:</h4>
                    <ul>
                    {% for strength in artifact.strengths %}
                        <li>{{ strength }}</li>
                    {% endfor %}
                    </ul>
                    
                    <h4>Critical Gaps:</h4>
                    <ul>
                    {% for gap in artifact.gaps %}
                        <li><strong>{{ gap.severity }}:</strong> {{ gap.gap }} <em>(Signals: {{ gap.linked_signals | join(', ') }})</em></li>
                    {% endfor %}
                    </ul>
                    
                    <h4>Priority Recommendations:</h4>
                    <ol>
                    {% for rec in artifact.recommendations %}
                        <li>
                            <strong>{{ rec.action }}</strong> ({{ rec.timeline }})
                            <br><em>{{ rec.rationale }}</em>
                            <br>Effort: {{ rec.effort }} | Impact: {{ rec.impact }} | Signals: {{ rec.linked_signals | join(', ') }}
                            {% if rec.references %}
                            <br>References: {{ rec.references | join(', ') }}
                            {% endif %}
                        </li>
                    {% endfor %}
                    </ol>
                    
                    <h4>Industry Benchmarks:</h4>
                    <ul>
                    {% for benchmark in artifact.benchmarks %}
                        <li><strong>{{ benchmark.control }}</strong> ({{ benchmark.framework }}): {{ benchmark.status }}
                        {% if benchmark.reference %} - {{ benchmark.reference }}{% endif %}
                        </li>
                    {% endfor %}
                    </ul>
                    
                    <p><em>Confidence Score: {{ "%.0f"|format(artifact.confidence_score * 100) }}%</em></p>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        
        <!-- Prioritized Recommendations Roadmap -->
        <div class="section page-break">
            <h2 id="recommendations">Prioritized Recommendations Roadmap</h2>
            <p>Based on the assessment results and AI analysis, here is a prioritized action plan organized by timeline and impact.</p>
            
            <h3>30-Day Quick Wins (High Impact, Low Effort)</h3>
            <table class="roadmap-table">
                <thead>
                    <tr>
                        <th style="width: 10%;">Priority</th>
                        <th style="width: 40%;">Action</th>
                        <th style="width: 15%;">Effort</th>
                        <th style="width: 15%;">Impact</th>
                        <th style="width: 20%;">Owner</th>
                    </tr>
                </thead>
                <tbody>
                    {% for rec in roadmap_30_day %}
                    <tr>
                        <td class="priority-{{ rec.priority }}">{{ rec.priority }}</td>
                        <td>{{ rec.action }}</td>
                        <td>{{ rec.effort }}</td>
                        <td>{{ rec.impact }}</td>
                        <td>{{ rec.owner }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <h3>60-Day Strategic Improvements</h3>
            <table class="roadmap-table">
                <thead>
                    <tr>
                        <th style="width: 10%;">Priority</th>
                        <th style="width: 40%;">Action</th>
                        <th style="width: 15%;">Effort</th>
                        <th style="width: 15%;">Impact</th>
                        <th style="width: 20%;">Owner</th>
                    </tr>
                </thead>
                <tbody>
                    {% for rec in roadmap_60_day %}
                    <tr>
                        <td class="priority-{{ rec.priority }}">{{ rec.priority }}</td>
                        <td>{{ rec.action }}</td>
                        <td>{{ rec.effort }}</td>
                        <td>{{ rec.impact }}</td>
                        <td>{{ rec.owner }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <h3>90-Day Long-Term Initiatives</h3>
            <table class="roadmap-table">
                <thead>
                    <tr>
                        <th style="width: 10%;">Priority</th>
                        <th style="width: 40%;">Action</th>
                        <th style="width: 15%;">Effort</th>
                        <th style="width: 15%;">Impact</th>
                        <th style="width: 20%;">Owner</th>
                    </tr>
                </thead>
                <tbody>
                    {% for rec in roadmap_90_day %}
                    <tr>
                        <td class="priority-{{ rec.priority }}">{{ rec.priority }}</td>
                        <td>{{ rec.action }}</td>
                        <td>{{ rec.effort }}</td>
                        <td>{{ rec.impact }}</td>
                        <td>{{ rec.owner }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <!-- Disclaimer & AI Transparency -->
        <div class="section page-break">
            <h2 id="disclaimer">Disclaimer & AI Transparency</h2>
            
            <h3>AI Analysis Transparency</h3>
            <div class="methodology-box">
                <p><strong>AI Model Used:</strong> {{ ai_model }}</p>
                <p><strong>Data Sources:</strong> Your questionnaire responses, industry security frameworks (NIST Cybersecurity Framework, ISO/IEC 27001, OWASP), and security best practices</p>
                <p><strong>Analysis Confidence:</strong> AI-generated insights are based on pattern recognition and industry benchmarks. Confidence levels vary by domain based on response completeness and clarity.</p>
                <p><strong>Limitations:</strong> AI analysis provides general guidance and may not account for organization-specific context, regulatory requirements, or unique business constraints. Professional security review is recommended for comprehensive planning.</p>
            </div>
            
            <h3>Report Disclaimer</h3>
            <p>This AI-enhanced security posture assessment provides advanced analysis based on industry best practices and AI-powered insights. The assessment and AI analysis are provided for informational purposes and should be validated by qualified security professionals.</p>
            
            <p>This report represents a point-in-time assessment based on the responses provided. Security posture is dynamic and should be reassessed regularly (recommended: quarterly) to account for evolving threats, technology changes, and business growth.</p>
            
            <p><strong>For comprehensive security architecture planning, incident response preparation, or detailed professional assessment, please contact EchoStor's security team.</strong></p>
            
            <p style="margin-top: 20px; font-size: 10px; color: #666;">
                <strong>Report ID:</strong> {{ report_id }}<br>
                <strong>Generated:</strong> {{ report_date }}<br>
                <strong>Assessment Period:</strong> {{ assessment.started_at.strftime('%Y-%m-%d') }} to {{ assessment.completed_at.strftime('%Y-%m-%d') }}<br>
                <strong>Classification:</strong> Confidential
            </p>
        </div>
        </div>
    </body>
    </html>
    """
    )

    overall_percentage = scores["overall"]["percentage"]
    if overall_percentage >= 80:
        overall_score_class = "high-score"
        overall_assessment = (
            "Strong security posture with good coverage across most areas."
        )
    elif overall_percentage >= 60:
        overall_score_class = "medium-score"
        overall_assessment = (
            "Moderate security posture with room for improvement in several areas."
        )
    else:
        overall_score_class = "low-score"
        overall_assessment = (
            "Security posture needs significant improvement across multiple areas."
        )

    # Generate prioritized roadmap
    roadmap = generate_prioritized_roadmap(scores, structure)

    return template.render(
        assessment=assessment,
        scores=scores,
        structure=structure,
        ai_insights=ai_insights,
        report_date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        report_id=assessment.id,
        overall_score_class=overall_score_class,
        overall_assessment=overall_assessment,
        roadmap_30_day=roadmap["30_day"],
        roadmap_60_day=roadmap["60_day"],
        roadmap_90_day=roadmap["90_day"],
        ai_model=settings.OPENAI_MODEL,
        get_maturity_level=get_maturity_level,
    )


def generate_recommendations(scores: dict[str, Any], structure: Any) -> list[str]:
    """Generate recommendations based on scores"""

    recommendations = []

    section_scores = [
        (section.title, scores[section.id]["percentage"])
        for section in structure.sections
    ]
    section_scores.sort(key=lambda x: x[1])

    for title, percentage in section_scores[:3]:
        if percentage < 70:
            recommendations.append(
                f"Prioritize improvements in {title} (current score: {percentage:.1f}%)"
            )

    overall_percentage = scores["overall"]["percentage"]
    if overall_percentage < 60:
        recommendations.append(
            "Consider engaging a cybersecurity consultant for comprehensive security program development"
        )

    if overall_percentage < 80:
        recommendations.append(
            "Implement regular security awareness training for all employees"
        )
        recommendations.append(
            "Establish a formal incident response plan and test it regularly"
        )

    return recommendations


def normalize_answer_display(answer_value: Any, question: Question) -> str:
    """Convert answer value to human-readable display format"""

    if answer_value is None:
        return "Not answered"

    if question.type == "yes_no":
        if isinstance(answer_value, bool):
            return "Yes" if answer_value else "No"
        if isinstance(answer_value, str):
            return "Yes" if answer_value.lower() in ["yes", "true", "1"] else "No"
        return "Yes" if answer_value else "No"

    elif question.type == "multiple_choice":
        if isinstance(answer_value, str):
            for option in question.options:
                if option.value == answer_value:
                    return option.label
        return str(answer_value) if answer_value else "Not answered"

    elif question.type == "multiple_select":
        if isinstance(answer_value, list) and answer_value:
            labels = []
            for val in answer_value:
                for option in question.options:
                    if option.value == val:
                        labels.append(option.label)
                        break
                else:
                    labels.append(str(val))
            return ", ".join(labels) if labels else "Not answered"
        return "Not answered"

    elif question.type == "text":
        if isinstance(answer_value, str) and answer_value.strip():
            return answer_value.replace("\n", "<br>")
        return "Not answered"

    return str(answer_value) if answer_value else "Not answered"


def get_maturity_level(percentage: float) -> str:
    """Get maturity level description for a score percentage"""
    if percentage >= 80:
        return "Strong"
    elif percentage >= 60:
        return "Moderate"
    elif percentage >= 40:
        return "Developing"
    else:
        return "Needs Improvement"


def get_maturity_tier(percentage: float) -> tuple[str, str]:
    """Get maturity tier and CSS class for a score percentage"""
    if percentage >= 80:
        return ("Strong", "high-score")
    elif percentage >= 60:
        return ("Moderate", "medium-score")
    else:
        return ("Needs Improvement", "low-score")


def generate_prioritized_roadmap(
    scores: dict[str, Any], structure: Any
) -> dict[str, list[dict[str, str]]]:
    """Generate prioritized roadmap organized by 30/60/90 day timelines"""

    roadmap_30_day = []
    roadmap_60_day = []
    roadmap_90_day = []

    section_scores = [
        (section.title, section.id, scores[section.id]["percentage"])
        for section in structure.sections
    ]
    section_scores.sort(key=lambda x: x[2])

    for title, _section_id, percentage in section_scores:
        if percentage < 40:
            roadmap_30_day.append(
                {
                    "priority": "p1",
                    "action": f"Implement foundational security controls in {title}",
                    "effort": "High",
                    "impact": "Critical",
                    "owner": "Security Team",
                }
            )
        elif percentage < 60:
            roadmap_30_day.append(
                {
                    "priority": "p2",
                    "action": f"Address critical gaps in {title}",
                    "effort": "Medium",
                    "impact": "High",
                    "owner": "Security Team",
                }
            )
        elif percentage < 70:
            roadmap_60_day.append(
                {
                    "priority": "p2",
                    "action": f"Strengthen controls in {title}",
                    "effort": "Medium",
                    "impact": "Medium",
                    "owner": "IT Team",
                }
            )
        elif percentage < 80:
            roadmap_90_day.append(
                {
                    "priority": "p3",
                    "action": f"Optimize and mature {title} practices",
                    "effort": "Low",
                    "impact": "Medium",
                    "owner": "IT Team",
                }
            )

    overall_percentage = scores["overall"]["percentage"]
    if overall_percentage < 60:
        roadmap_30_day.insert(
            0,
            {
                "priority": "p1",
                "action": "Engage cybersecurity consultant for comprehensive security program development",
                "effort": "Medium",
                "impact": "Critical",
                "owner": "Executive Team",
            },
        )

    if overall_percentage < 80:
        roadmap_60_day.append(
            {
                "priority": "p2",
                "action": "Implement regular security awareness training for all employees",
                "effort": "Medium",
                "impact": "High",
                "owner": "HR/Security Team",
            }
        )
        roadmap_60_day.append(
            {
                "priority": "p2",
                "action": "Establish and test formal incident response plan",
                "effort": "High",
                "impact": "High",
                "owner": "Security Team",
            }
        )

    roadmap_90_day.append(
        {
            "priority": "p3",
            "action": "Conduct quarterly security posture reassessment",
            "effort": "Low",
            "impact": "Medium",
            "owner": "Security Team",
        }
    )

    if not roadmap_30_day:
        roadmap_30_day.append(
            {
                "priority": "p3",
                "action": "Maintain current security controls and monitor for emerging threats",
                "effort": "Low",
                "impact": "Medium",
                "owner": "Security Team",
            }
        )

    if not roadmap_60_day:
        roadmap_60_day.append(
            {
                "priority": "p3",
                "action": "Review and update security policies and procedures",
                "effort": "Medium",
                "impact": "Medium",
                "owner": "Security Team",
            }
        )

    return {
        "30_day": roadmap_30_day[:5],
        "60_day": roadmap_60_day[:5],
        "90_day": roadmap_90_day[:5],
    }


def calculate_confidence_level(scores: dict) -> tuple[str, str]:
    """Calculate overall confidence level based on completion rates"""

    total_completion = 0
    section_count = 0

    for key, value in scores.items():
        if key != "overall" and "completion_rate" in value:
            total_completion += value["completion_rate"]
            section_count += 1

    avg_completion = total_completion / section_count if section_count > 0 else 0

    if avg_completion >= 80:
        return ("High", "All sections substantially completed with reliable results")
    elif avg_completion >= 60:
        return ("Medium", "Most sections completed, results generally reliable")
    else:
        return ("Low", "Significant gaps in completion may affect result reliability")


def generate_prioritized_remediation(scores: dict, structure: Any) -> list[dict]:
    """Generate prioritized remediation plan with effort and timeframe"""

    remediation_items = []

    section_scores = [
        (section, scores[section.id]["percentage"]) for section in structure.sections
    ]
    section_scores.sort(key=lambda x: x[1])

    for section, percentage in section_scores[:5]:
        if percentage < 70:
            priority = "P1" if percentage < 50 else "P2"
            effort = "High" if percentage < 40 else "Medium"
            timeframe = "90-180 days" if percentage < 40 else "30-90 days"

            remediation_items.append(
                {
                    "domain": section.title,
                    "priority": priority,
                    "effort": effort,
                    "timeframe": timeframe,
                    "current_score": f"{percentage:.1f}%",
                }
            )

    for section, percentage in section_scores:
        if 60 <= percentage < 80:
            remediation_items.append(
                {
                    "domain": section.title,
                    "priority": "P3",
                    "effort": "Low",
                    "timeframe": "0-30 days",
                    "current_score": f"{percentage:.1f}%",
                }
            )
            if len(remediation_items) >= 10:
                break

    return remediation_items


def generate_section_summaries(
    scores: dict, structure: Any, responses: list
) -> list[dict]:
    """Generate summary for each section with strengths and gaps"""

    response_dict = {r.question_id: r for r in responses}
    summaries = []

    for section in structure.sections:
        section_score = scores[section.id]

        answered_questions = []
        for question in section.questions:
            response = response_dict.get(question.id)
            if response:
                answered_questions.append((question, response))

        strengths = []
        gaps = []

        for question, response in answered_questions:
            if question.type == "yes_no":
                answer_str = str(response.answer_value).lower()
                if answer_str in ["yes", "true", "1"]:
                    if question.weight >= 4:
                        strengths.append(
                            question.text[:80] + "..."
                            if len(question.text) > 80
                            else question.text
                        )
                else:
                    if question.weight >= 4:
                        gaps.append(
                            question.text[:80] + "..."
                            if len(question.text) > 80
                            else question.text
                        )

        # Generate recommendations
        recommendations = []
        if section_score["percentage"] < 70:
            recommendations.append(
                f"Focus on improving {section.title} - current score below target"
            )
        if section_score["completion_rate"] < 100:
            recommendations.append(
                f"Complete remaining {section_score['total_questions'] - section_score['responses_count']} questions"
            )
        if section_score["percentage"] >= 80:
            recommendations.append(
                "Maintain current strong practices and review periodically"
            )

        summaries.append(
            {
                "section": section,
                "score": section_score["percentage"],
                "completion": section_score["completion_rate"],
                "strengths": strengths[:3],  # Top 3
                "gaps": gaps[:3],  # Top 3
                "recommendations": recommendations[:3],  # Top 3
            }
        )

    return summaries
