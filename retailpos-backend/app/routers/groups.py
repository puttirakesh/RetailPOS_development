"""Group CRUD – JWT required."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.group import GroupCreate, GroupListResponse, GroupRead, GroupUpdate
from app.services.group import GroupService

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("", response_model=GroupListResponse)
def list_groups(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
    search: str | None = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> GroupListResponse:
    return GroupService(db).list_items(search=search, skip=skip, limit=limit)


@router.get("/{group_id}", response_model=GroupRead)
def get_group(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> GroupRead:
    return GroupService(db).get(group_id)


@router.post("", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
def create_group(
    body: GroupCreate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> GroupRead:
    return GroupService(db).create(body)


@router.put("/{group_id}", response_model=GroupRead)
def update_group(
    group_id: int,
    body: GroupUpdate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> GroupRead:
    return GroupService(db).update(group_id, body)


@router.delete("/{group_id}")
def delete_group(
    group_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> dict[str, str]:
    return GroupService(db).delete(group_id)