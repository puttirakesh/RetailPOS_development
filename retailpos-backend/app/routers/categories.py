"""Category CRUD – JWT required."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryListResponse,
    CategoryRead,
    CategoryUpdate,
)
from app.services.category import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=CategoryListResponse)
def list_categories(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
    active_only: bool = Query(True),
    group_id: int | None = Query(None, gt=0),
    search: str | None = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> CategoryListResponse:
    return CategoryService(db).list_items(
        active_only=active_only,
        group_id=group_id,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(
    category_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> CategoryRead:
    return CategoryService(db).get(category_id)


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    body: CategoryCreate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> CategoryRead:
    return CategoryService(db).create(body)


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    body: CategoryUpdate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> CategoryRead:
    return CategoryService(db).update(category_id, body)


@router.delete("/{category_id}", response_model=CategoryRead)
def delete_category(
    category_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> CategoryRead:
    return CategoryService(db).delete(category_id)