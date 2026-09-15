"""TaxMaster business logic. TaxId is IDENTITY from SQL Server."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.tax import TaxRepository
from app.schemas.tax import TaxCreate, TaxListResponse, TaxRead, TaxUpdate


class TaxService:
    def __init__(self, db: Session) -> None:
        self.repo = TaxRepository(db)

    def list_items(
        self, *, active_only: bool = True, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> TaxListResponse:
        items = self.repo.get_all(active_only=active_only, search=search, skip=skip, limit=limit)
        total = self.repo.count(active_only=active_only, search=search)
        return TaxListResponse(total=total, items=[TaxRead.model_validate(i) for i in items])

    def get(self, tax_id: int) -> TaxRead:
        row = self.repo.get_by_id(tax_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Tax {tax_id} not found")
        return TaxRead.model_validate(row)

    def create(self, payload: TaxCreate) -> TaxRead:
        if self.repo.get_by_name(payload.tax_name):
            raise HTTPException(status_code=409, detail=f"Tax name '{payload.tax_name}' exists")
        row = self.repo.create(
            tax_name=payload.tax_name,
            tax_percentage=payload.tax_percentage,
            tax_type=payload.tax_type,
            is_active=payload.is_active,
        )
        return TaxRead.model_validate(row)

    def update(self, tax_id: int, payload: TaxUpdate) -> TaxRead:
        row = self.repo.get_by_id(tax_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Tax {tax_id} not found")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")
        if "tax_name" in data and self.repo.get_by_name(data["tax_name"], exclude_id=tax_id):
            raise HTTPException(status_code=409, detail=f"Tax name '{data['tax_name']}' exists")
        for k, v in data.items():
            setattr(row, k, v)
        return TaxRead.model_validate(self.repo.update(row))

    def delete(self, tax_id: int) -> TaxRead:
        row = self.repo.get_by_id(tax_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Tax {tax_id} not found")
        if not row.is_active:
            raise HTTPException(status_code=409, detail=f"Tax {tax_id} already inactive")
        return TaxRead.model_validate(self.repo.soft_delete(row))