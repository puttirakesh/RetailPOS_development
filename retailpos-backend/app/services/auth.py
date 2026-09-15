"""Authentication business logic."""

from __future__ import annotations

from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logging import get_logger
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    needs_rehash,
    verify_password,
)
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import TokenResponse

logger = get_logger(__name__)


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)

    def authenticate(self, username: str, password: str) -> User:
        user = self.users.get_by_username(username.strip())
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        if needs_rehash(user.password):
            try:
                hashed = hash_password(password)
                self.users.update_password(user, hashed)
                logger.info("password_upgraded_to_bcrypt user_id=%s", user.user_id)
            except Exception as exc:
                self.db.rollback()
                logger.warning(
                    "password_upgrade_failed user_id=%s error=%s",
                    user.user_id,
                    exc,
                )

        return user

    def issue_tokens(self, user: User) -> TokenResponse:
        access = create_access_token(
            subject=user.username,
            role=user.role,
            user_id=user.user_id,
        )
        refresh = create_refresh_token(
            subject=user.username,
            user_id=user.user_id,
        )
        return TokenResponse(
            access_token=access,
            refresh_token=refresh,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            role=user.role,
            username=user.username,
            user_id=user.user_id,
        )

    def refresh(self, refresh_token: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        user_id = payload.get("uid")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        user = self.users.get_by_id(int(user_id))
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
            )

        return self.issue_tokens(user)