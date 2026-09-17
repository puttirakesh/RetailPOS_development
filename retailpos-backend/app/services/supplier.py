"""Supplier business logic."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.supplier import SupplierRepository
from app.schemas.supplier import (
    SupplierCreate,
    SupplierListResponse,
    SupplierRead,
    SupplierUpdate,
)


class SupplierService:
    def __init__(self, db: Session) -> None:
        self.repo = SupplierRepository(db)

    def list_items(
        self, *, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> SupplierListResponse:
        items = self.repo.get_all(search=search, skip=skip, limit=limit)
        total = self.repo.count(search=search)
        return SupplierListResponse(
            total=total, items=[SupplierRead.model_validate(i) for i in items]
        )

    def get(self, supplier_id: int) -> SupplierRead:
        row = self.repo.get_by_id(supplier_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Supplier {supplier_id} not found")
        return SupplierRead.model_validate(row)

    def create(self, payload: SupplierCreate) -> SupplierRead:
        supplier_id = self.repo.next_id()
        code = payload.supplier_code or str(supplier_id)
        row = self.repo.create(
            supplier_id=supplier_id,
            supplier_code=code,
            supplier_name=payload.supplier_name,
            mobile_no=payload.mobile_no,
            address=payload.address,
            city_id=payload.city_id,
            state_id=payload.state_id,
            gst_no=payload.gst_no or "",
        )
        return SupplierRead.model_validate(row)

    def update(self, supplier_id: int, payload: SupplierUpdate) -> SupplierRead:
        row = self.repo.get_by_id(supplier_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Supplier {supplier_id} not found")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")
        for k, v in data.items():
            setattr(row, k, v)
        return SupplierRead.model_validate(self.repo.update(row))

    def delete(self, supplier_id: int) -> dict[str, str]:
        row = self.repo.get_by_id(supplier_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Supplier {supplier_id} not found")
        self.repo.delete(row)
        return {"detail": f"Supplier {supplier_id} deleted"}