"""Brand CRUD router – all endpoints require JWT."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.brand import BrandCreate, BrandListResponse, BrandRead, BrandUpdate
from app.services.brand import BrandService

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("", response_model=BrandListResponse, summary="List brands")
def list_brands(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
    active_only: bool = Query(True),
    search: str | None = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> BrandListResponse:
    return BrandService(db).list_brands(
        active_only=active_only, search=search, skip=skip, limit=limit
    )


@router.get("/{brand_id}", response_model=BrandRead, summary="Get brand")
def get_brand(
    brand_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> BrandRead:
    return BrandService(db).get_brand(brand_id)


@router.post("", response_model=BrandRead, status_code=status.HTTP_201_CREATED, summary="Create brand")
def create_brand(
    body: BrandCreate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> BrandRead:
    return BrandService(db).create_brand(body)


@router.put("/{brand_id}", response_model=BrandRead, summary="Update brand")
def update_brand(
    brand_id: int,
    body: BrandUpdate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> BrandRead:
    return BrandService(db).update_brand(brand_id, body)


@router.delete("/{brand_id}", response_model=BrandRead, summary="Soft-delete brand")
def delete_brand(
    brand_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> BrandRead:
    return BrandService(db).delete_brand(brand_id)