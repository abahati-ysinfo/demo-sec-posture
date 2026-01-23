"""
Prompt builder for AI intake recommendations.
Constructs system and user messages for OpenAI API calls.
"""

import json
from typing import Any

from app.schemas.intake import SectionMetadata, UserProfile

INTAKE_PROMPT_VERSION = "v1"


def build_system_message() -> str:
    """Build the system message for OpenAI"""
    return """You are an experienced cybersecurity architect helping organisations decide which security assessment sections are most relevant to them.

You are given:
* A brief user profile (role, organisation size, sector, environment, goals).
* A list of available assessment sections with names, descriptions and tags.

Your task:
* Recommend which sections the user should complete NOW, to get the most value for their time.
* Prioritise sections based on:
  * The user's environment (cloud vs on-prem, OT/ICS, custom apps, etc.).
  * The user's goals (overall posture, compliance, cloud focus, etc.).
  * The time they are willing to spend (quick vs moderate vs deep dive).
* If a section is clearly not applicable (e.g. OT/ICS for a SaaS-only company), call that out in `excluded_sections`.

You MUST:
* Respond with STRICT, VALID JSON only.
* Use only the section IDs provided.
* Assign each recommended section a priority: "must_do", "should_do" or "optional".
* Provide a short reason for each recommendation or exclusion.
* Set confidence scores between 0.0 and 1.0 for each recommendation."""


def build_user_message(
    user_profile: UserProfile, sections: list[SectionMetadata]
) -> str:
    """Build the user message with profile and sections data"""

    profile_dict = user_profile.model_dump()
    sections_list = [section.model_dump() for section in sections]

    message = f"""Here is the user's profile (JSON):

{json.dumps(profile_dict, indent=2)}

Here are the available assessment sections (JSON):

{json.dumps(sections_list, indent=2)}

Based on this user's context, goals and time preference:

1. Recommend which sections they should complete now.
2. Prioritise them as:
   - "must_do" for the most critical ones,
   - "should_do" for important but secondary ones,
   - "optional" for nice-to-have sections.
3. If any sections are clearly not applicable, include them in "excluded_sections" with a reason.

Respond with JSON ONLY in this exact structure:

{{
  "recommended_sections": [
    {{
      "id": "section_4",
      "priority": "must_do",
      "reason": "Identity and access management is critical for all organisations and especially important for hybrid cloud environments.",
      "confidence": 0.95
    }}
  ],
  "excluded_sections": [
    {{
      "id": "section_18",
      "reason": "User does not have OT/ICS or industrial control systems, so this section provides little value.",
      "confidence": 0.99
    }}
  ]
}}

No extra text, comments or explanations outside the JSON."""

    return message


def build_messages(
    user_profile: UserProfile, sections: list[SectionMetadata]
) -> list[dict[str, str]]:
    """Build the complete messages array for OpenAI API"""
    return [
        {"role": "system", "content": build_system_message()},
        {"role": "user", "content": build_user_message(user_profile, sections)},
    ]


def get_openai_params() -> dict[str, Any]:
    """Get OpenAI API parameters for intake recommendations"""
    return {
        "model": "gpt-4o-mini",
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
