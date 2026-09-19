"""Product CRUD – JWT required."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductListResponse,
    ProductRead,
    ProductUpdate,
)
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListResponse)
def list_products(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
    active_only: bool = Query(True),
    category_id: int | None = Query(None, gt=0),
    search: str | None = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> ProductListResponse:
    return ProductService(db).list_items(
        active_only=active_only,
        category_id=category_id,
        search=search,
        skip=skip,
        limit=limit,
    )


@router.get("/{product_id}", response_model=ProductRead)
def get_product(
    product_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> ProductRead:
    return ProductService(db).get(product_id)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    body: ProductCreate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> ProductRead:
    return ProductService(db).create(body)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    body: ProductUpdate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> ProductRead:
    return ProductService(db).update(product_id, body)


@router.delete("/{product_id}", response_model=ProductRead)
def delete_product(
    product_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> ProductRead:
    return ProductService(db).delete(product_id)