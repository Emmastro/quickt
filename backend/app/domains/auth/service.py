import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    decode_password_reset_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)

from .models import User
from .schemas import TokenResponse, UserRegister, UserUpdatePreferences

logger = logging.getLogger("quickt.auth")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, data: UserRegister) -> tuple[User, TokenResponse]:
        result = await self.db.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            raise ConflictError("Email already registered")

        user = User(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
            phone=data.phone,
            city=data.city,
            role=data.role,
        )
        self.db.add(user)
        await self.db.flush()

        tokens = TokenResponse(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )
        return user, tokens

    async def login(self, email: str, password: str) -> tuple[User, TokenResponse]:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is deactivated")

        tokens = TokenResponse(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )
        return user, tokens

    async def refresh(self, refresh_token_str: str) -> TokenResponse:
        payload = decode_refresh_token(refresh_token_str)
        if payload is None:
            raise UnauthorizedError("Invalid or expired refresh token")

        user_id = payload["sub"]
        result = await self.db.execute(
            select(User).where(User.id == user_id, User.is_active.is_(True))
        )
        user = result.scalar_one_or_none()
        if not user:
            raise UnauthorizedError("User not found")

        return TokenResponse(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )

    async def request_password_reset(self, email: str) -> str | None:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            return None
        return create_password_reset_token(str(user.id))

    async def reset_password(self, token: str, new_password: str) -> User:
        payload = decode_password_reset_token(token)
        if payload is None:
            raise BadRequestError("Invalid or expired reset token")

        user_id = payload["sub"]
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user or not user.is_active:
            raise BadRequestError("Invalid or expired reset token")

        user.hashed_password = hash_password(new_password)
        await self.db.flush()
        return user

    async def update_preferences(self, user: User, data: UserUpdatePreferences) -> User:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        await self.db.flush()
        return user
