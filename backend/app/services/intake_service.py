"""
Intake recommendation service.
Handles AI-powered section recommendations with fallback logic and guardrails.
"""

import json
import logging
from typing import Any

import openai
from sqlalchemy.orm import Session

from app.models.intake import IntakeSession
from app.schemas.intake import (
    AIRecommendationResponse,
    IntakeAnswers,
    IntakeRecommendationResponse,
    SectionExclusion,
    SectionMetadata,
    SectionRecommendation,
    UserProfile,
)
from app.services.intake_prompt_builder import (
    build_messages,
    get_openai_params,
)
from app.services.openai_key_manager import OpenAIKeyManager

logger = logging.getLogger(__name__)


def load_sections_metadata() -> list[SectionMetadata]:
    """Load section metadata from JSON file"""
    import os

    current_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    metadata_path = os.path.join(current_dir, "data", "sections_metadata.json")

    with open(metadata_path, encoding="utf-8") as f:
        data = json.load(f)

    return [SectionMetadata(**section) for section in data]


def map_answers_to_profile(answers: IntakeAnswers) -> UserProfile:
    """Convert intake answers to structured user profile"""
    has_ot_ics = "ot_ics" in answers.system_types

    return UserProfile(
        role=answers.role,
        org_size=answers.org_size,
        sector=answers.sector,
        environment=answers.environment,
        system_types=answers.system_types,
        has_ot_ics=has_ot_ics,
        cloud_providers=answers.cloud_providers,
        primary_goal=answers.primary_goal,
        primary_goal_detail=answers.primary_goal_detail,
        time_preference=answers.time_preference,
    )


def call_openai_for_recommendations(
    user_profile: UserProfile,
    sections: list[SectionMetadata],
    key_manager: OpenAIKeyManager,
) -> tuple[AIRecommendationResponse | None, dict[str, Any] | None]:
    """
    Call OpenAI API to get section recommendations.
    Returns (parsed_response, raw_response_dict) or (None, None) on failure.
    """
    key_id: str | None = None
    api_key: str | None = None

    try:
        key_id, api_key = key_manager.get_next_key()
        if not key_id or not api_key:
            logger.error("No available OpenAI API keys")
            return None, None

        messages = build_messages(user_profile, sections)
        params = get_openai_params()

        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            messages=messages,  # type: ignore
            **params,
        )

        content = response.choices[0].message.content
        if not content:
            logger.error("Empty response from OpenAI")
            key_manager.record_failure(key_id, Exception("Empty response from OpenAI"))
            return None, None

        try:
            raw_dict = json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse OpenAI response as JSON: {e}")
            key_manager.record_failure(key_id, e)
            return None, None

        try:
            ai_response = AIRecommendationResponse(**raw_dict)
        except Exception as e:
            logger.error(f"Failed to validate OpenAI response structure: {e}")
            key_manager.record_failure(key_id, e)
            return None, None

        key_manager.record_success(key_id)

        return ai_response, raw_dict

    except openai.APITimeoutError as e:
        logger.error(f"OpenAI API timeout: {e}")
        if key_id:
            key_manager.record_failure(key_id, e)
        return None, None
    except openai.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        if key_id:
            key_manager.record_failure(key_id, e)
        return None, None
    except Exception as e:
        logger.error(f"Unexpected error calling OpenAI: {e}")
        if key_id:
            key_manager.record_failure(key_id, e)
        return None, None


def generate_fallback_recommendations(
    user_profile: UserProfile, sections: list[SectionMetadata]
) -> AIRecommendationResponse:
    """
    Generate deterministic fallback recommendations based on user profile.
    Used when AI fails or returns invalid data.
    """
    recommended = []
    excluded = []

    sections_by_id = {s.id: s for s in sections}

    core_sections = [
        "section_1",
        "section_4",
        "section_10",
    ]  # Governance, IAM, Incident Response
    for section_id in core_sections:
        if section_id in sections_by_id:
            recommended.append(
                SectionRecommendation(
                    id=section_id,
                    priority="must_do",
                    reason=f"{sections_by_id[section_id].name} is critical for all organizations.",
                    confidence=0.9,
                )
            )

    if user_profile.cloud_providers and "none" not in [
        p.lower() for p in user_profile.cloud_providers
    ]:
        if "section_9" in sections_by_id:
            recommended.append(
                SectionRecommendation(
                    id="section_9",
                    priority="must_do",
                    reason="Cloud security is essential for organizations using cloud platforms.",
                    confidence=0.95,
                )
            )

    if user_profile.has_ot_ics:
        if "section_18" in sections_by_id:
            recommended.append(
                SectionRecommendation(
                    id="section_18",
                    priority="must_do",
                    reason="OT/ICS security is critical for organizations with industrial control systems.",
                    confidence=0.95,
                )
            )
    else:
        if "section_18" in sections_by_id:
            excluded.append(
                SectionExclusion(
                    id="section_18",
                    reason="Organization does not have OT/ICS or industrial control systems.",
                    confidence=0.99,
                )
            )

    if (
        "public_web_apps" in user_profile.system_types
        or "internal_custom_apps" in user_profile.system_types
    ):
        if "section_8" in sections_by_id:
            recommended.append(
                SectionRecommendation(
                    id="section_8",
                    priority="should_do",
                    reason="Application security is important for organizations with custom or web applications.",
                    confidence=0.85,
                )
            )

    if (
        "overall" in user_profile.primary_goal.lower()
        or "posture" in user_profile.primary_goal.lower()
    ):
        if "section_2" in sections_by_id:
            recommended.append(
                SectionRecommendation(
                    id="section_2",
                    priority="should_do",
                    reason="Risk management helps understand overall security posture.",
                    confidence=0.85,
                )
            )

    if "section_7" in sections_by_id:
        recommended.append(
            SectionRecommendation(
                id="section_7",
                priority="should_do",
                reason="Data protection is important for most organizations.",
                confidence=0.8,
            )
        )

    if user_profile.time_preference == "quick":
        recommended = [r for r in recommended if r.priority == "must_do"][:5]
    elif user_profile.time_preference == "moderate":
        recommended = recommended[:8]

    return AIRecommendationResponse(
        recommended_sections=recommended,
        excluded_sections=excluded,
    )


def apply_guardrails(
    ai_response: AIRecommendationResponse,
    user_profile: UserProfile,
    sections: list[SectionMetadata],
) -> AIRecommendationResponse:
    """
    Apply hard business rules to AI recommendations.
    Ensures critical sections are included based on user profile.
    """
    sections_by_id = {s.id: s for s in sections}
    recommended_ids = {r.id for r in ai_response.recommended_sections}

    if "section_4" not in recommended_ids and "section_4" in sections_by_id:
        ai_response.recommended_sections.append(
            SectionRecommendation(
                id="section_4",
                priority="must_do",
                reason="Identity & Access Management is critical for all organizations (added by guardrail).",
                confidence=0.95,
            )
        )
        recommended_ids.add("section_4")

    if user_profile.cloud_providers and "none" not in [
        p.lower() for p in user_profile.cloud_providers
    ]:
        if "section_9" not in recommended_ids and "section_9" in sections_by_id:
            found = False
            for rec in ai_response.recommended_sections:
                if rec.id == "section_9":
                    if rec.priority != "must_do":
                        rec.priority = "must_do"
                        rec.reason += " (upgraded by guardrail)"
                    found = True
                    break
            if not found:
                ai_response.recommended_sections.append(
                    SectionRecommendation(
                        id="section_9",
                        priority="should_do",
                        reason="Cloud security is important for organizations using cloud platforms (added by guardrail).",
                        confidence=0.9,
                    )
                )
                recommended_ids.add("section_9")

    if user_profile.has_ot_ics:
        if "section_18" not in recommended_ids and "section_18" in sections_by_id:
            ai_response.excluded_sections = [
                e for e in ai_response.excluded_sections if e.id != "section_18"
            ]
            ai_response.recommended_sections.append(
                SectionRecommendation(
                    id="section_18",
                    priority="must_do",
                    reason="OT/ICS security is critical for organizations with industrial control systems (added by guardrail).",
                    confidence=0.95,
                )
            )
            recommended_ids.add("section_18")

    if user_profile.time_preference == "quick":
        must_do = [
            r for r in ai_response.recommended_sections if r.priority == "must_do"
        ]
        should_do = [
            r for r in ai_response.recommended_sections if r.priority == "should_do"
        ]
        optional = [
            r for r in ai_response.recommended_sections if r.priority == "optional"
        ]

        should_do.sort(key=lambda x: x.confidence or 0.5, reverse=True)
        optional.sort(key=lambda x: x.confidence or 0.5, reverse=True)

        final = must_do[:5]
        remaining = 5 - len(final)
        if remaining > 0:
            final.extend(should_do[:remaining])

        ai_response.recommended_sections = final

    elif user_profile.time_preference == "moderate":
        must_do = [
            r for r in ai_response.recommended_sections if r.priority == "must_do"
        ]
        should_do = [
            r for r in ai_response.recommended_sections if r.priority == "should_do"
        ]
        optional = [
            r for r in ai_response.recommended_sections if r.priority == "optional"
        ]

        should_do.sort(key=lambda x: x.confidence or 0.5, reverse=True)
        optional.sort(key=lambda x: x.confidence or 0.5, reverse=True)

        final = must_do[:8]
        remaining = 8 - len(final)
        if remaining > 0:
            final.extend(should_do[:remaining])
            remaining = 8 - len(final)
            if remaining > 0:
                final.extend(optional[:remaining])

        ai_response.recommended_sections = final

    valid_ids = set(sections_by_id.keys())
    ai_response.recommended_sections = [
        r for r in ai_response.recommended_sections if r.id in valid_ids
    ]
    ai_response.excluded_sections = [
        e for e in ai_response.excluded_sections if e.id in valid_ids
    ]

    return ai_response


def generate_recommendations(
    answers: IntakeAnswers,
    db: Session,
    user_id: str | None = None,
) -> IntakeRecommendationResponse:
    """
    Main function to generate section recommendations.
    Handles AI call, fallback, guardrails, and persistence.
    """
    sections = load_sections_metadata()

    user_profile = map_answers_to_profile(answers)

    used_fallback = False
    ai_response = None
    raw_response = None

    try:
        key_manager = OpenAIKeyManager(db)
        ai_response, raw_response = call_openai_for_recommendations(
            user_profile, sections, key_manager
        )

        if ai_response is None:
            logger.info("First OpenAI call failed, retrying once...")
            ai_response, raw_response = call_openai_for_recommendations(
                user_profile, sections, key_manager
            )

    except Exception as e:
        logger.error(f"Error in OpenAI recommendation flow: {e}")

    if ai_response is None:
        logger.warning("Using fallback recommendations due to AI failure")
        ai_response = generate_fallback_recommendations(user_profile, sections)
        used_fallback = True
    else:
        ai_response = apply_guardrails(ai_response, user_profile, sections)

    session = IntakeSession(
        user_id=user_id,
        user_profile_json=user_profile.model_dump(),
        ai_raw_response_json=raw_response,
        final_selected_section_ids=[r.id for r in ai_response.recommended_sections],
        time_preference=user_profile.time_preference,
        used_fallback=used_fallback,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return IntakeRecommendationResponse(
        recommended_sections=ai_response.recommended_sections,
        excluded_sections=ai_response.excluded_sections,
        used_fallback=used_fallback,
        session_id=str(session.id),
    )
