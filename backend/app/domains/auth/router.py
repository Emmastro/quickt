from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.email import load_template, send_email
from app.database import get_db
from app.dependencies import get_current_user

from .models import User
from .schemas import (
    ForgotPasswordRequest,
    MessageResponse,
    ResetPasswordRequest,
    TokenResponse,
    UserLogin,
    UserPublic,
    UserRegister,
    UserUpdatePreferences,
)
from .service import AuthService

router = APIRouter()
bearer_scheme = HTTPBearer()


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    svc = AuthService(db)
    _, tokens = await svc.register(data)
    return tokens


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    svc = AuthService(db)
    _, tokens = await svc.login(data.email, data.password)
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    svc = AuthService(db)
    return await svc.refresh(credentials.credentials)


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(data: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    svc = AuthService(db)
    token = await svc.request_password_reset(data.email)
    if token:
        settings = get_settings()
        reset_link = f"{settings.frontend_url}/reset-password?token={token}"
        html = load_template(
            "password_reset",
            USER_NAME=data.email,
            USER_EMAIL=data.email,
            RESET_LINK=reset_link,
        )
        await send_email(
            to=data.email,
            subject="QuickT — Reinitialisation du mot de passe",
            html_body=html,
        )
    return MessageResponse(message="If an account with that email exists, a reset link has been sent.")


@router.get("/me", response_model=UserPublic)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserPublic)
async def update_preferences(
    data: UserUpdatePreferences,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    svc = AuthService(db)
    return await svc.update_preferences(current_user, data)
