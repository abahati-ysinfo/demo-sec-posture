from typing import Annotated

from pydantic import BaseModel, Field


class IntakeAnswers(BaseModel):
    """User's answers to the discovery questionnaire"""

    role: Annotated[str, Field(min_length=1, max_length=200)]
    org_size: Annotated[str, Field(min_length=1, max_length=50)]
    sector: Annotated[str, Field(min_length=1, max_length=200)]
    environment: Annotated[str, Field(min_length=1, max_length=100)]
    system_types: list[Annotated[str, Field(min_length=1, max_length=100)]]
    cloud_providers: list[Annotated[str, Field(min_length=1, max_length=100)]]
    primary_goal: Annotated[str, Field(min_length=1, max_length=500)]
    primary_goal_detail: Annotated[str, Field(max_length=2000)] | None = None
    time_preference: Annotated[str, Field(pattern="^(quick|moderate|deep)$")]


class UserProfile(BaseModel):
    """Structured user profile derived from intake answers"""

    role: str
    org_size: str
    sector: str
    environment: str
    system_types: list[str]
    has_ot_ics: bool
    cloud_providers: list[str]
    primary_goal: str
    primary_goal_detail: str | None = None
    time_preference: str


class SectionMetadata(BaseModel):
    """Metadata about an assessment section"""

    id: str
    name: str
    description: str
    tags: list[str]


class SectionRecommendation(BaseModel):
    """AI recommendation for a single section"""

    id: str
    priority: Annotated[str, Field(pattern="^(must_do|should_do|optional)$")]
    reason: Annotated[str, Field(min_length=1, max_length=1000)]
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] | None = None


class SectionExclusion(BaseModel):
    """AI exclusion for a single section"""

    id: str
    reason: Annotated[str, Field(min_length=1, max_length=1000)]
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] | None = None


class AIRecommendationResponse(BaseModel):
    """Structured response from OpenAI"""

    recommended_sections: list[SectionRecommendation]
    excluded_sections: list[SectionExclusion] = Field(default_factory=list)


class IntakeRecommendationResponse(BaseModel):
    """Final recommendation response sent to frontend"""

    recommended_sections: list[SectionRecommendation]
    excluded_sections: list[SectionExclusion]
    used_fallback: bool
    session_id: str


class SubmitIntakeRequest(BaseModel):
    """Request to submit intake answers and get recommendations"""

    answers: IntakeAnswers


class DiscoveryQuestion(BaseModel):
    """A single discovery question"""

    id: str
    text: str
    type: Annotated[str, Field(pattern="^(single_select|multi_select|text)$")]
    options: list[dict[str, str]] | None = None
    required: bool = True


class DiscoveryQuestionnaire(BaseModel):
    """Complete discovery questionnaire"""

    questions: list[DiscoveryQuestion]
