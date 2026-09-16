"""State CRUD – JWT required."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.state import StateCreate, StateListResponse, StateRead, StateUpdate
from app.services.state import StateService

router = APIRouter(prefix="/states", tags=["States"])


@router.get("", response_model=StateListResponse)
def list_states(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
    active_only: bool = Query(True),
    search: str | None = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> StateListResponse:
    return StateService(db).list_items(
        active_only=active_only, search=search, skip=skip, limit=limit
    )


@router.get("/{state_id}", response_model=StateRead)
def get_state(
    state_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> StateRead:
    return StateService(db).get(state_id)


@router.post("", response_model=StateRead, status_code=status.HTTP_201_CREATED)
def create_state(
    body: StateCreate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> StateRead:
    return StateService(db).create(body)


@router.put("/{state_id}", response_model=StateRead)
def update_state(
    state_id: int,
    body: StateUpdate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> StateRead:
    return StateService(db).update(state_id, body)


@router.delete("/{state_id}", response_model=StateRead)
def delete_state(
    state_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> StateRead:
    return StateService(db).delete(state_id)