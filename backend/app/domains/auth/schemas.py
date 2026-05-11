from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    phone: str
    city: str | None = None
    role: str = "customer"


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    phone: str
    full_name: str
    role: str
    city: str | None
    preferred_language: str
    agency_id: int | None = None
    is_active: bool
    created_at: datetime


class UserUpdatePreferences(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    city: str | None = None
    preferred_language: str | None = None


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class MessageResponse(BaseModel):
    message: str
