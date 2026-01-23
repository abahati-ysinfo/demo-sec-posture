"""Schemas for OpenAI API key management."""

from datetime import datetime

from pydantic import BaseModel, Field


class OpenAIKeyCreate(BaseModel):
    """Schema for creating a new OpenAI API key."""

    key_name: str = Field(..., min_length=1, max_length=255)
    api_key: str = Field(..., min_length=20)


class OpenAIKeyResponse(BaseModel):
    """Schema for OpenAI API key response."""

    id: str
    key_name: str
    masked_key: str
    is_active: bool
    last_used_at: datetime | None
    usage_count: int
    cooldown_until: datetime | None
    error_count: int
    created_at: datetime
    created_by: str

    class Config:
        from_attributes = True


class OpenAIKeyToggle(BaseModel):
    """Schema for toggling key active status."""

    is_active: bool


class OpenAIKeyTest(BaseModel):
    """Schema for testing an API key."""

    api_key: str = Field(..., min_length=20)


class OpenAIKeyTestResponse(BaseModel):
    """Schema for API key test response."""

    is_valid: bool
    message: str
