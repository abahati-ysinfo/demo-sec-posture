import re
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    email: EmailStr
    full_name: Annotated[str, Field(min_length=1, max_length=100)]
    company_name: Annotated[str, Field(min_length=1, max_length=200)]


class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=8, max_length=128)]

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserUpdate(BaseModel):
    full_name: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    company_name: Annotated[str, Field(min_length=1, max_length=200)] | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: str
    is_active: bool
    is_admin: bool
    is_protected: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CurrentUserResponse(BaseModel):
    """Unified response model for current user (from get_current_user)"""

    id: str
    email: EmailStr
    full_name: str | None = None
    company_name: str | None = None
    is_admin: bool
    is_active: bool = True

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse | None = None
    is_admin: bool | None = None
    csrf_token: str | None = None


class TokenData(BaseModel):
    email: str | None = None
    is_admin: bool = False


class BulkUpdateUserStatusRequest(BaseModel):
    user_ids: Annotated[list[str], Field(min_length=1, max_length=100)]
    is_active: bool


class BulkDeleteUsersRequest(BaseModel):
    user_ids: Annotated[list[str], Field(min_length=1, max_length=100)]
