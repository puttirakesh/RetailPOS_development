"""UOM business logic."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.uom import UomRepository
from app.schemas.uom import UomCreate, UomListResponse, UomRead, UomUpdate


class UomService:
    def __init__(self, db: Session) -> None:
        self.repo = UomRepository(db)

    def list_items(
        self, *, active_only: bool = True, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> UomListResponse:
        items = self.repo.get_all(active_only=active_only, search=search, skip=skip, limit=limit)
        total = self.repo.count(active_only=active_only, search=search)
        return UomListResponse(total=total, items=[UomRead.model_validate(i) for i in items])

    def get(self, uom_id: int) -> UomRead:
        row = self.repo.get_by_id(uom_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"UOM {uom_id} not found")
        return UomRead.model_validate(row)

    def create(self, payload: UomCreate) -> UomRead:
        if self.repo.get_by_code(payload.uom_code):
            raise HTTPException(status_code=409, detail=f"UOM code '{payload.uom_code}' exists")
        if self.repo.get_by_name(payload.uom_name):
            raise HTTPException(status_code=409, detail=f"UOM name '{payload.uom_name}' exists")
        uom_id = self.repo.next_id()
        row = self.repo.create(
            uom_id=uom_id,
            uom_code=payload.uom_code,
            uom_name=payload.uom_name,
            is_active=payload.is_active,
        )