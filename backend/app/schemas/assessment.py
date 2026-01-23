import uuid
from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserSummary(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    company_name: str

    class Config:
        from_attributes = True


class AssessmentBase(BaseModel):
    status: (
        Annotated[str, Field(pattern="^(in_progress|completed|expired)$")] | None
    ) = "in_progress"


class AssessmentCreate(AssessmentBase):
    selected_section_ids: (
        list[Annotated[str, Field(min_length=1, max_length=100)]] | None
    ) = None

    @field_validator("selected_section_ids")
    @classmethod
    def validate_selected_section_ids(cls, v: list[str] | None) -> list[str] | None:
        if v is not None:
            if len(v) == 0:
                raise ValueError("At least one section must be selected")
            if len(v) != len(set(v)):
                raise ValueError("Duplicate section IDs are not allowed")
        return v


class AssessmentUpdate(BaseModel):
    status: (
        Annotated[str, Field(pattern="^(in_progress|completed|expired)$")] | None
    ) = None
    completed_at: datetime | None = None
    progress_percentage: Annotated[float, Field(ge=0, le=100)] | None = None


class AssessmentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    attempt_number: int = 1
    status: str
    started_at: datetime
    completed_at: datetime | None
    expires_at: datetime | None
    last_saved_at: datetime
    progress_percentage: float
    selected_section_ids: list[str] | None = None
    consultation_interest: bool = False
    consultation_details: Annotated[str, Field(max_length=5000)] | None = None
    user: UserSummary | None = None

    class Config:
        from_attributes = True


class AssessmentResponseCreate(BaseModel):
    section_id: Annotated[str, Field(min_length=1, max_length=100)]
    question_id: Annotated[str, Field(min_length=1, max_length=100)]
    answer_value: Any
    comment: Annotated[str, Field(max_length=2000)] | None = None

    @field_validator("answer_value")
    @classmethod
    def validate_answer_value(cls, v: Any) -> Any:
        if v is None:
            raise ValueError("answer_value cannot be None")
        if isinstance(v, str):
            if len(v) > 5000:
                raise ValueError("String answer_value cannot exceed 5000 characters")
            if len(v.strip()) == 0:
                raise ValueError("String answer_value cannot be empty")
        elif isinstance(v, list):
            if len(v) > 100:
                raise ValueError("List answer_value cannot exceed 100 items")
            for item in v:
                if isinstance(item, str) and len(item) > 1000:
                    raise ValueError("List items cannot exceed 1000 characters")
        return v


class AssessmentResponseUpdate(BaseModel):
    answer_value: Any

    @field_validator("answer_value")
    @classmethod
    def validate_answer_value(cls, v: Any) -> Any:
        if v is None:
            raise ValueError("answer_value cannot be None")
        if isinstance(v, str):
            if len(v) > 5000:
                raise ValueError("String answer_value cannot exceed 5000 characters")
            if len(v.strip()) == 0:
                raise ValueError("String answer_value cannot be empty")
        elif isinstance(v, list):
            if len(v) > 100:
                raise ValueError("List answer_value cannot exceed 100 items")
        return v


class AssessmentResponseResponse(BaseModel):
    id: uuid.UUID
    assessment_id: uuid.UUID
    section_id: str
    question_id: str
    answer_value: Any
    comment: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SaveProgressRequest(BaseModel):
    responses: Annotated[
        list[AssessmentResponseCreate], Field(min_length=1, max_length=500)
    ]


class ConsultationRequest(BaseModel):
    consultation_interest: bool
    consultation_details: Annotated[str, Field(max_length=5000)] | None = None

    @field_validator("consultation_details")
    @classmethod
    def validate_consultation_details(cls, v: str | None, info: Any) -> str | None:
        consultation_interest = info.data.get("consultation_interest", False)

        if v is not None and not v.strip():
            return None

        if consultation_interest and v and v.strip():
            word_count = len(v.split())
            if word_count < 10:
                raise ValueError(
                    f"Consultation details must be at least 10 words (currently {word_count} words)"
                )
            if word_count > 300:
                raise ValueError(
                    f"Consultation details must not exceed 300 words (currently {word_count} words)"
                )

        return v


class OptionExplanation(BaseModel):
    """Detailed explanation for a question option"""

    definition: Annotated[str, Field(max_length=2000)] | None = None
    why_matters: Annotated[str, Field(max_length=2000)] | None = None
    industry_adoption_rate: Annotated[str, Field(max_length=500)] | None = None
    industry_benchmark: Annotated[str, Field(max_length=1000)] | None = None
    compliance_frameworks: Annotated[str, Field(max_length=1000)] | None = None
    recommendation: Annotated[str, Field(max_length=2000)] | None = None
    path_to_improvement: Annotated[str, Field(max_length=2000)] | None = None


class QuestionOption(BaseModel):
    value: Annotated[str, Field(min_length=1, max_length=200)]
    label: Annotated[str, Field(min_length=1, max_length=500)]
    description: Annotated[str, Field(max_length=1000)] | None = None
    detailed_explanation: OptionExplanation | None = None


class Question(BaseModel):
    id: Annotated[str, Field(min_length=1, max_length=100)]
    section_id: Annotated[str, Field(min_length=1, max_length=100)]
    text: Annotated[str, Field(min_length=1, max_length=2000)]
    type: Annotated[
        str, Field(pattern="^(yes_no|multiple_choice|multiple_select|text)$")
    ]
    weight: Annotated[int, Field(ge=0, le=100)]
    explanation: Annotated[str, Field(max_length=5000)]
    options: list[QuestionOption]
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def scale_type(self) -> str | None:
        """Get scale type from metadata"""
        return self.metadata.get("scale_type")


class Section(BaseModel):
    id: Annotated[str, Field(min_length=1, max_length=100)]
    title: Annotated[str, Field(min_length=1, max_length=500)]
    description: Annotated[str, Field(max_length=2000)]
    questions: list[Question]


class AssessmentStructure(BaseModel):
    sections: Annotated[list[Section], Field(min_length=1)]
    total_questions: Annotated[int, Field(ge=0)]
