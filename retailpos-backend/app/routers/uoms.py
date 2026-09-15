"""UOM CRUD – JWT required."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.uom import UomCreate, UomListResponse, UomRead, UomUpdate
from app.services.uom import UomService

router = APIRouter(prefix="/uoms", tags=["UOMs"])


@router.get("", response_model=UomListResponse)
def list_uoms(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
    active_only: bool = Query(True),
    search: str | None = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> UomListResponse:
    return UomService(db).list_items(
        active_only=active_only, search=search, skip=skip, limit=limit
    )


@router.get("/{uom_id}", response_model=UomRead)
def get_uom(
    uom_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> UomRead:
    return UomService(db).get(uom_id)


@router.post("", response_model=UomRead, status_code=status.HTTP_201_CREATED)
def create_uom(
    body: UomCreate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> UomRead:
    return UomService(db).create(body)


@router.put("/{uom_id}", response_model=UomRead)
def update_uom(
    uom_id: int,
    body: UomUpdate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> UomRead:
    return UomService(db).update(uom_id, body)


@router.delete("/{uom_id}", response_model=UomRead)
def delete_uom(
    uom_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> UomRead:
    return UomService(db).delete(uom_id)