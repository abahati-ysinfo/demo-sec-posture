"""AI Synthesis Service for cross-section analysis and executive summary"""

import logging
import time
from typing import Any

from openai import AsyncOpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.ai_artifacts import SectionAIArtifact, SynthesisArtifact
from app.services.benchmark_context import benchmark_context_service
from app.services.openai_key_manager import OpenAIKeyManager
from app.utils.openai_helpers import get_temperature_param, get_token_params

logger = logging.getLogger(__name__)


def build_synthesis_prompt(
    section_summaries: list[dict[str, Any]],
    overall_score: float,
    curated_context: str = "",
) -> str:
    """Build prompt for cross-section synthesis"""

    summaries_text = []
    for summary in section_summaries:
        summaries_text.append(
            f"""
Section: {summary["title"]} (Score: {summary["score"]}%)
Risk Level: {summary["risk_level"]}
Top Gaps: {", ".join(summary["top_gaps"][:3])}
Top Recommendations: {", ".join(summary["top_recommendations"][:3])}
"""
        )

    prompt = f"""You are a cybersecurity executive advisor. Analyze these section summaries from a comprehensive security assessment and provide strategic synthesis.

OVERALL SECURITY SCORE: {overall_score}%

SECTION SUMMARIES:
{"".join(summaries_text)}

{curated_context}

Provide your synthesis as JSON matching this schema:

{{
  "executive_summary": "2-3 paragraph overview for C-level executives highlighting current posture, key risks, and strategic recommendations",
  
  "overall_risk_level": "Low|Medium|Medium-High|High|Critical",
  "overall_risk_explanation": "Detailed explanation of overall risk considering all domains",
  
  "cross_cutting_themes": [
    {{
      "theme": "Identity and Access Management Gaps",
      "description": "Detailed description of the theme",
      "affected_domains": ["identity", "access_control", "network"],
      "severity": "High"
    }}
  ],
  
  "top_10_initiatives": [
    {{
      "priority": 1,
      "title": "Implement Enterprise-Wide MFA",
      "description": "Deploy multi-factor authentication across all systems and user accounts",
      "affected_domains": ["identity", "access_control"],
      "effort": "Medium",
      "impact": "Critical",
      "timeline": "30-day",
      "dependencies": [],
      "success_metrics": ["100% MFA adoption", "Zero password-only accounts", "MFA enforcement in all critical systems"],
      "owner": "Security Team"
    }}
  ],
  
  "quick_wins": [
    "Enable MFA for all admin accounts (1 week)",
    "Implement automated patch management (2 weeks)",
    "Deploy endpoint protection on all devices (1 week)"
  ],
  
  "long_term_strategy": "Strategic direction for next 6-12 months including maturity progression, team building, and program development",
  
  "confidence_score": 0.85
}}

REQUIREMENTS:
1. Executive summary must be business-focused, not technical
2. Identify 3-5 cross-cutting themes that span multiple domains
3. Prioritize initiatives by: (impact × urgency) / effort
4. Map dependencies: higher-priority items that must complete before others
5. Success metrics must be specific and measurable
6. Quick wins must be achievable in <30 days with low effort
7. Long-term strategy should align with industry best practices

Keep response professional and actionable for executive audience.
"""
    return prompt


async def generate_synthesis_artifact(
    section_artifacts: dict[str, SectionAIArtifact],
    structure: Any,
    scores: dict[str, Any],
    key_manager: OpenAIKeyManager,
    db: Session,
) -> SynthesisArtifact:
    """Generate cross-section synthesis"""

    section_summaries = []
    for section in structure.sections:
        artifact = section_artifacts.get(section.id)
        if artifact:
            section_summaries.append(
                {
                    "title": section.title,
                    "score": scores[section.id]["percentage"],
                    "risk_level": artifact.risk_level,
                    "top_gaps": [g.gap for g in artifact.gaps[:3]],
                    "top_recommendations": [
                        r.action for r in artifact.recommendations[:3]
                    ],
                }
            )

    curated_context = benchmark_context_service.get_relevant_context(
        "Executive Security Strategy",
        "Overall security posture and strategic initiatives",
        max_controls=10,
    )

    prompt = build_synthesis_prompt(
        section_summaries, scores["overall"]["percentage"], curated_context
    )

    try:
        key_id, api_key = key_manager.get_next_key()
        client = AsyncOpenAI(api_key=api_key, timeout=settings.OPENAI_TIMEOUT)

        start_time = time.time()
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            **get_temperature_param(0.5),
            **get_token_params(2000),  # Longer for synthesis
        )
        latency_ms = int((time.time() - start_time) * 1000)

        json_str = response.choices[0].message.content
        if json_str:
            synthesis = SynthesisArtifact.model_validate_json(json_str)
        else:
            raise ValueError("Empty response from OpenAI")

        key_manager.record_success(key_id)

        logger.info(f"Generated synthesis artifact ({latency_ms}ms)")
        return synthesis

    except Exception as e:
        logger.error(f"Failed to generate synthesis: {e}")
        if key_manager:
            key_manager.record_failure(key_id, e)

        return create_minimal_synthesis(scores["overall"]["percentage"])


def create_minimal_synthesis(overall_score: float) -> SynthesisArtifact:
    """Create minimal synthesis when AI fails"""
    # Ensure strings meet minimum length requirements from schema
    executive_summary = (
        f"Security assessment completed with overall score of {overall_score:.1f}%. "
        "Detailed analysis is available in the section-by-section breakdown below. "
        "AI-powered synthesis is temporarily unavailable. Please review individual "
        "section analyses for specific findings, gaps, and recommendations. "
        "Contact support if you need assistance with interpreting the results."
    )
    overall_risk_explanation = (
        "Manual review of section analyses is recommended to understand the full "
        "security posture. Each section contains detailed findings that should be "
        "reviewed by qualified security personnel."
    )
    long_term_strategy = (
        "Conduct a comprehensive security program review with a qualified consultant "
        "to develop a tailored roadmap. Focus on addressing critical gaps identified "
        "in individual sections and establishing a continuous improvement process "
        "for security maturity advancement."
    )
    return SynthesisArtifact(
        schema_version="1.0",
        executive_summary=executive_summary,
        overall_risk_level="Medium" if overall_score >= 60 else "High",
        overall_risk_explanation=overall_risk_explanation,
        cross_cutting_themes=[],
        top_10_initiatives=[],
        quick_wins=["Review section-by-section recommendations"],
        long_term_strategy=long_term_strategy,
        confidence_score=0.0,
    )
