"""Enhanced Executive Summary Generation Service"""

import logging
import time
from typing import Any

from openai import AsyncOpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.ai_artifacts import SectionAIArtifact, SynthesisArtifact
from app.services.openai_key_manager import OpenAIKeyManager
from app.utils.openai_helpers import get_token_params

logger = logging.getLogger(__name__)


def build_enhanced_executive_summary_prompt(
    section_artifacts: dict[str, SectionAIArtifact],
    synthesis_artifact: SynthesisArtifact,
    scores: dict[str, Any],
    structure: Any,
    assessment: Any,
) -> str:
    """Build prompt for enhanced executive summary generation"""

    # Build section snapshot with defensive guards
    section_snapshot = []
    for section in structure.sections:
        section_score = scores.get(section.id, {})
        artifact = section_artifacts.get(section.id)

        # Defensive: check if percentage exists in section_score
        if section_score and artifact and "percentage" in section_score:
            section_snapshot.append(
                f"- {section.title}: {section_score['percentage']:.1f}% (Risk: {artifact.risk_level})"
            )

    # Build key strengths summary
    strengths_summary = []
    for section in structure.sections:
        artifact = section_artifacts.get(section.id)
        if artifact and artifact.strengths:
            top_strength = artifact.strengths[0] if artifact.strengths else None
            if top_strength:
                strengths_summary.append(f"- {section.title}: {top_strength}")

    # Build key gaps summary
    gaps_summary = []
    for section in structure.sections:
        artifact = section_artifacts.get(section.id)
        if artifact and artifact.gaps:
            # Get highest severity gap
            critical_gaps = [
                g for g in artifact.gaps if g.severity in ["Critical", "High"]
            ]
            if critical_gaps:
                top_gap = critical_gaps[0]
                gaps_summary.append(
                    f"- {section.title}: {top_gap.gap} (Severity: {top_gap.severity})"
                )

    # Build themes summary with defensive guards
    themes_summary = []
    cross_cutting_themes = synthesis_artifact.cross_cutting_themes or []
    for theme in cross_cutting_themes[:5]:
        themes_summary.append(
            f"- {theme.theme} (Severity: {theme.severity}): {theme.description[:150]}..."
        )

    # Build top initiatives summary (top 5) with defensive guards
    initiatives_summary = []
    top_10_initiatives = synthesis_artifact.top_10_initiatives or []
    for initiative in top_10_initiatives[:5]:
        initiatives_summary.append(
            f"- Priority {initiative.priority}: {initiative.title} "
            f"(Effort: {initiative.effort}, Impact: {initiative.impact}, Timeline: {initiative.timeline})"
        )

    # Get assessment metadata with defensive guards
    assessment_date = (
        assessment.completed_at.strftime("%B %d, %Y")
        if assessment.completed_at
        else "N/A"
    )
    num_sections = len(structure.sections)
    overall_score = scores.get("overall", {}).get("percentage", 0.0)
    overall_risk = synthesis_artifact.overall_risk_level

    prompt = f"""You are a cybersecurity executive advisor writing a comprehensive one-page executive summary for C-level and board stakeholders.

ASSESSMENT CONTEXT:
- Assessment completed: {assessment_date}
- Scope: {num_sections} security domains assessed
- Overall security score: {overall_score:.1f}%
- Overall risk level: {overall_risk}

SECTION SCORES AND RISK LEVELS:
{chr(10).join(section_snapshot[:15])}

KEY STRENGTHS BY DOMAIN:
{chr(10).join(strengths_summary[:8])}

KEY GAPS AND RISKS BY DOMAIN:
{chr(10).join(gaps_summary[:8])}

CROSS-CUTTING THEMES:
{chr(10).join(themes_summary)}

TOP PRIORITY INITIATIVES:
{chr(10).join(initiatives_summary)}

QUICK WINS (30-DAY ACTIONS):
{chr(10).join(f"- {win}" for win in (synthesis_artifact.quick_wins or []))}

LONG-TERM STRATEGIC DIRECTION:
{synthesis_artifact.long_term_strategy}

OVERALL RISK EXPLANATION:
{synthesis_artifact.overall_risk_explanation}

TASK:
Write a comprehensive executive summary suitable as the FIRST section of a board-ready security assessment report.

AUDIENCE: Non-technical executives, CEO, CISO, board members

LENGTH: Approximately 250-350 words (compact but comprehensive, aim for fitting on a single page when rendered as PDF)

TONE: 
- Concise and business-focused
- Neutral and objective
- Professional and authoritative
- Avoid technical jargon; use business language

STRUCTURE: Use Markdown formatting with the following sections and structure:

## Executive Overview
Write 2-3 paragraphs that provide:
- Context: What was assessed, when, and scope
- Current state: Overall security posture and maturity
- Key message: The most important takeaway for executives

## Current Security Posture
- Overall score and what it means in business terms
- Risk level and implications
- 2-3 key strengths to celebrate
- 3-4 critical gaps that need immediate attention

## Strategic Priorities
Summarize the top 3-5 initiatives from the priority list above, focusing on:
- Business impact and risk reduction
- Resource requirements (effort/timeline)
- Dependencies and sequencing

## Immediate Actions (Next 30 Days)
List 2-3 quick wins that can demonstrate progress quickly

## 6-12 Month Roadmap
Summarize the long-term strategy in 2-3 sentences, focusing on:
- Maturity progression
- Key milestones
- Expected outcomes

## Recommended Next Steps
Provide 2-3 concrete next steps for leadership, such as:
- Schedule roadmap review meeting
- Approve budget for priority initiatives
- Establish governance structure
- Engage with security leadership

REQUIREMENTS:
1. Do not invent data that is not supported by the inputs above
2. Use business language, not technical jargon
3. Focus on risk, impact, and business value
4. Be specific with numbers and timelines where provided
5. Maintain professional, objective tone
6. Use markdown formatting (##, -, **bold**) for structure
7. Keep total length to approximately 500-700 words

Generate the enhanced executive summary now:"""

    return prompt


async def generate_enhanced_executive_summary(
    section_artifacts: dict[str, SectionAIArtifact],
    synthesis_artifact: SynthesisArtifact,
    scores: dict[str, Any],
    structure: Any,
    assessment: Any,
    key_manager: OpenAIKeyManager,
    db: Session,
) -> str:
    """Generate enhanced executive summary using AI"""

    prompt = build_enhanced_executive_summary_prompt(
        section_artifacts, synthesis_artifact, scores, structure, assessment
    )

    key_id: str | None = None
    try:
        key_id, api_key = key_manager.get_next_key()
        client = AsyncOpenAI(api_key=api_key, timeout=settings.OPENAI_TIMEOUT)

        start_time = time.time()
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,  # Balanced creativity and consistency
            **get_token_params(1500),  # Dedicated token budget for executive summary
        )
        latency_ms = int((time.time() - start_time) * 1000)

        enhanced_summary = response.choices[0].message.content
        if not enhanced_summary:
            raise ValueError("Empty response from OpenAI")

        key_manager.record_success(key_id)

        # Normalize and enforce length constraints
        raw_summary = enhanced_summary.strip()
        raw_len = len(raw_summary)
        logger.info(f"Enhanced executive summary raw length: {raw_len} chars")

        # Schema constraints from SynthesisArtifact
        MAX_LEN = 2000
        MIN_LEN = 200

        if raw_len > MAX_LEN:
            logger.warning(
                f"Enhanced executive summary too long ({raw_len} > {MAX_LEN}); truncating"
            )
            raw_summary = raw_summary[:MAX_LEN]

        if len(raw_summary) < MIN_LEN:
            logger.warning(
                f"Enhanced executive summary too short ({len(raw_summary)} < {MIN_LEN}); using original"
            )
            return synthesis_artifact.executive_summary

        logger.info(
            f"Enhanced executive summary generated ({latency_ms}ms, final length: {len(raw_summary)} chars)"
        )
        return raw_summary

    except Exception as e:
        logger.error(
            f"Failed to generate enhanced executive summary: {e}", exc_info=True
        )
        if key_id is not None:
            key_manager.record_failure(key_id, e)

        # Fallback to original executive summary
        logger.warning("Using original executive summary as fallback")
        return synthesis_artifact.executive_summary
