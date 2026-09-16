"""State business logic."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.state import StateRepository
from app.schemas.state import StateCreate, StateListResponse, StateRead, StateUpdate


class StateService:
    def __init__(self, db: Session) -> None:
        self.repo = StateRepository(db)

    def list_items(
        self, *, active_only: bool = True, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> StateListResponse:
        items = self.repo.get_all(active_only=active_only, search=search, skip=skip, limit=limit)
        total = self.repo.count(active_only=active_only, search=search)
        return StateListResponse(total=total, items=[StateRead.model_validate(i) for i in items])

    def get(self, state_id: int) -> StateRead:
        row = self.repo.get_by_id(state_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"State {state_id} not found")
        return StateRead.model_validate(row)

    def create(self, payload: StateCreate) -> StateRead:
        if self.repo.get_by_code(payload.state_code):
            raise HTTPException(status_code=409, detail=f"State code '{payload.state_code}' exists")
        state_id = self.repo.next_id()
        row = self.repo.create(
            state_id=state_id,
            state_code=payload.state_code,
            state_name=payload.state_name,
            state_type=payload.state_type,
            is_active=payload.is_active,
        )
        return StateRead.model_validate(row)

    def update(self, state_id: int, payload: StateUpdate) -> StateRead:
        row = self.repo.get_by_id(state_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"State {state_id} not found")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")
        if "state_code" in data and self.repo.get_by_code(data["state_code"], exclude_id=state_id):
            raise HTTPException(status_code=409, detail=f"State code '{data['state_code']}' exists")
        for k, v in data.items():
            setattr(row, k, v)
        return StateRead.model_validate(self.repo.update(row))

    def delete(self, state_id: int) -> StateRead:
        row = self.repo.get_by_id(state_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"State {state_id} not found")
        if not row.is_active:
            raise HTTPException(status_code=409, detail=f"State {state_id} already inactive")
        return StateRead.model_validate(self.repo.soft_delete(row))