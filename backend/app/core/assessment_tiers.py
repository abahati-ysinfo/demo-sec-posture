"""
Assessment tier definitions for Quick/Standard/Deep assessment modes
"""

from typing import TypedDict


class TierInfo(TypedDict, total=False):
    """Type definition for assessment tier information"""

    name: str
    description: str
    duration: str
    total_questions: int
    sections: list[str] | str  # Can be list of section IDs or "all"


ASSESSMENT_TIERS: dict[str, TierInfo] = {
    "quick": {
        "name": "Quick Check",
        "description": "Essential security fundamentals (15-25 questions)",
        "duration": "10-15 minutes",
        "sections": [
            "section_1",  # Governance & Strategy (7 questions)
            "section_4",  # Identity & Access Management (8 questions)
            "section_10",  # Incident Response & Resilience (6 questions)
        ],
        "total_questions": 21,  # Approximate
    },
    "standard": {
        "name": "Standard Assessment",
        "description": "Comprehensive security evaluation (80-120 questions)",
        "duration": "45-60 minutes",
        "sections": [
            "section_1",  # Governance & Strategy
            "section_2",  # Risk Management
            "section_3",  # Asset Management
            "section_4",  # Identity & Access Management
            "section_5",  # Network Security
            "section_7",  # Data Protection & Privacy
            "section_8",  # Application Security
            "section_10",  # Incident Response & Resilience
            "section_15",  # Monitoring & Detection
            "section_16",  # Vulnerability Management
        ],
        "total_questions": 95,  # Approximate
    },
    "deep": {
        "name": "Deep Dive Assessment",
        "description": "Complete security posture analysis (400+ questions)",
        "duration": "2-3 hours",
        "sections": "all",  # All 19 sections
        "total_questions": 409,
    },
}


def get_tier_sections(tier: str) -> list[str]:
    """Get section IDs for a tier"""
    if tier not in ASSESSMENT_TIERS:
        raise ValueError(f"Unknown tier: {tier}")

    tier_config = ASSESSMENT_TIERS[tier]

    sections = tier_config["sections"]
    if sections == "all":
        from app.services.question_parser import load_assessment_structure

        structure = load_assessment_structure()
        return [section.id for section in structure.sections]
    else:
        return sections  # type: ignore[return-value]


def get_tier_info(tier: str) -> TierInfo:
    """Get tier information for UI"""
    if tier not in ASSESSMENT_TIERS:
        raise ValueError(f"Unknown tier: {tier}")

    return ASSESSMENT_TIERS[tier]
