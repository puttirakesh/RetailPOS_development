"""City business logic."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.city import CityRepository
from app.repositories.state import StateRepository
from app.schemas.city import CityCreate, CityListResponse, CityRead, CityUpdate


class CityService:
    def __init__(self, db: Session) -> None:
        self.repo = CityRepository(db)
        self.states = StateRepository(db)

    def list_items(
        self,
        *,
        active_only: bool = True,
        state_id: int | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> CityListResponse:
        items = self.repo.get_all(
            active_only=active_only, state_id=state_id, search=search, skip=skip, limit=limit
        )
        total = self.repo.count(active_only=active_only, state_id=state_id, search=search)
        return CityListResponse(total=total, items=[CityRead.model_validate(i) for i in items])

    def get(self, city_id: int) -> CityRead:
        row = self.repo.get_by_id(city_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"City {city_id} not found")
        return CityRead.model_validate(row)

    def create(self, payload: CityCreate) -> CityRead:
        if self.states.get_by_id(payload.state_id) is None:
            raise HTTPException(status_code=400, detail=f"State {payload.state_id} does not exist")
        city_id = self.repo.next_id()
        row = self.repo.create(
            city_id=city_id,
            city_code=payload.city_code,
            city_name=payload.city_name,
            state_id=payload.state_id,
            is_active=payload.is_active,
        )
        return CityRead.model_validate(row)

    def update(self, city_id: int, payload: CityUpdate) -> CityRead:
        row = self.repo.get_by_id(city_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"City {city_id} not found")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")
        if "state_id" in data and self.states.get_by_id(data["state_id"]) is None:
            raise HTTPException(status_code=400, detail=f"State {data['state_id']} does not exist")
        for k, v in data.items():
            setattr(row, k, v)
        return CityRead.model_validate(self.repo.update(row))

    def delete(self, city_id: int) -> CityRead:
        row = self.repo.get_by_id(city_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"City {city_id} not found")
        if not row.is_active:
            raise HTTPException(status_code=409, detail=f"City {city_id} already inactive")
        return CityRead.model_validate(self.repo.soft_delete(row))