"""Authentication routes: login, refresh, me."""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse, UserPublic
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse, summary="Login")
def login(body: LoginRequest, db: Annotated[Session, Depends(get_db)]) -> TokenResponse:
    service = AuthService(db)
    user = service.authenticate(body.username, body.password)
    return service.issue_tokens(user)


@router.post("/refresh", response_model=TokenResponse, summary="Refresh tokens")
def refresh(
    body: RefreshRequest, db: Annotated[Session, Depends(get_db)]
) -> TokenResponse:
    service = AuthService(db)
    return service.refresh(body.refresh_token)


@router.get("/me", response_model=UserPublic, summary="Current user")
def me(user: Annotated[User, Depends(get_current_user)]) -> UserPublic:
    return UserPublic(
        user_id=user.user_id,
        username=user.username,
        role=user.role,
        is_active=user.is_active,
    )