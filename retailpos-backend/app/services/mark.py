"""Mark business logic."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.mark import MarkRepository
from app.schemas.mark import MarkCreate, MarkListResponse, MarkRead, MarkUpdate


class MarkService:
    def __init__(self, db: Session) -> None:
        self.repo = MarkRepository(db)

    def list_items(
        self, *, active_only: bool = True, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> MarkListResponse:
        items = self.repo.get_all(active_only=active_only, search=search, skip=skip, limit=limit)
        total = self.repo.count(active_only=active_only, search=search)
        return MarkListResponse(total=total, items=[MarkRead.model_validate(i) for i in items])

    def get(self, mark_id: int) -> MarkRead:
        row = self.repo.get_by_id(mark_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Mark {mark_id} not found")
        return MarkRead.model_validate(row)

    def create(self, payload: MarkCreate) -> MarkRead:
        mark_id = self.repo.next_id()
        row = self.repo.create(
            mark_id=mark_id,
            mark_code=payload.mark_code,
            mark_amount=payload.mark_amount,
            is_active=payload.is_active,
        )
        return MarkRead.model_validate(row)

    def update(self, mark_id: int, payload: MarkUpdate) -> MarkRead:
        row = self.repo.get_by_id(mark_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Mark {mark_id} not found")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")
        for k, v in data.items():
            setattr(row, k, v)
        return MarkRead.model_validate(self.repo.update(row))

    def delete(self, mark_id: int) -> MarkRead:
        row = self.repo.get_by_id(mark_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Mark {mark_id} not found")
        if not row.is_active:
            raise HTTPException(status_code=409, detail=f"Mark {mark_id} already inactive")
        return MarkRead.model_validate(self.repo.soft_delete(row))