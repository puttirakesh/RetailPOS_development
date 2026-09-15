"""TaxMaster CRUD – JWT required. TaxId is IDENTITY."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.tax import TaxCreate, TaxListResponse, TaxRead, TaxUpdate
from app.services.tax import TaxService

router = APIRouter(prefix="/taxes", tags=["Taxes"])


@router.get("", response_model=TaxListResponse)
def list_taxes(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
    active_only: bool = Query(True),
    search: str | None = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> TaxListResponse:
    return TaxService(db).list_items(
        active_only=active_only, search=search, skip=skip, limit=limit
    )


@router.get("/{tax_id}", response_model=TaxRead)
def get_tax(
    tax_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> TaxRead:
    return TaxService(db).get(tax_id)


@router.post("", response_model=TaxRead, status_code=status.HTTP_201_CREATED)
def create_tax(
    body: TaxCreate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> TaxRead:
    return TaxService(db).create(body)


@router.put("/{tax_id}", response_model=TaxRead)
def update_tax(
    tax_id: int,
    body: TaxUpdate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> TaxRead:
    return TaxService(db).update(tax_id, body)


@router.delete("/{tax_id}", response_model=TaxRead)
def delete_tax(
    tax_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> TaxRead:
    return TaxService(db).delete(tax_id)