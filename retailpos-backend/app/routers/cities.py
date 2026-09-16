"""City CRUD – JWT required."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.city import CityCreate, CityListResponse, CityRead, CityUpdate
from app.services.city import CityService

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("", response_model=CityListResponse)
def list_cities(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
    active_only: bool = Query(True),
    state_id: int | None = Query(None, gt=0),
    search: str | None = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> CityListResponse:
    return CityService(db).list_items(
        active_only=active_only, state_id=state_id, search=search, skip=skip, limit=limit
    )


@router.get("/{city_id}", response_model=CityRead)
def get_city(
    city_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> CityRead:
    return CityService(db).get(city_id)


@router.post("", response_model=CityRead, status_code=status.HTTP_201_CREATED)
def create_city(
    body: CityCreate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> CityRead:
    return CityService(db).create(body)


@router.put("/{city_id}", response_model=CityRead)
def update_city(
    city_id: int,
    body: CityUpdate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> CityRead:
    return CityService(db).update(city_id, body)


@router.delete("/{city_id}", response_model=CityRead)
def delete_city(
    city_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> CityRead:
    return CityService(db).delete(city_id)