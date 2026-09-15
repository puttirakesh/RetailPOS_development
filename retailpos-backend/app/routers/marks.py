"""Mark CRUD – JWT required."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.mark import MarkCreate, MarkListResponse, MarkRead, MarkUpdate
from app.services.mark import MarkService

router = APIRouter(prefix="/marks", tags=["Marks"])


@router.get("", response_model=MarkListResponse)
def list_marks(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
    active_only: bool = Query(True),
    search: str | None = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> MarkListResponse:
    return MarkService(db).list_items(
        active_only=active_only, search=search, skip=skip, limit=limit
    )


@router.get("/{mark_id}", response_model=MarkRead)
def get_mark(
    mark_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> MarkRead:
    return MarkService(db).get(mark_id)


@router.post("", response_model=MarkRead, status_code=status.HTTP_201_CREATED)
def create_mark(
    body: MarkCreate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> MarkRead:
    return MarkService(db).create(body)


@router.put("/{mark_id}", response_model=MarkRead)
def update_mark(
    mark_id: int,
    body: MarkUpdate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> MarkRead:
    return MarkService(db).update(mark_id, body)


@router.delete("/{mark_id}", response_model=MarkRead)
def delete_mark(
    mark_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> MarkRead:
    return MarkService(db).delete(mark_id)