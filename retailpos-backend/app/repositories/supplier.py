"""Supplier repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.supplier import Supplier


class SupplierRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self, *, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> list[Supplier]:
        stmt = select(Supplier).order_by(Supplier.supplier_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                (Supplier.supplier_name.ilike(term))
                | (Supplier.supplier_code.ilike(term))
                | (Supplier.mobile_no.ilike(term))
            )
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(self, *, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(Supplier)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                (Supplier.supplier_name.ilike(term))
                | (Supplier.supplier_code.ilike(term))
                | (Supplier.mobile_no.ilike(term))
            )
        return self.db.scalar(stmt) or 0

    def get_by_id(self, supplier_id: int) -> Supplier | None:
        return self.db.get(Supplier, supplier_id)

    def next_id(self) -> int:
        return int(self.db.scalar(select(func.max(Supplier.supplier_id))) or 0) + 1

    def create(self, **kwargs) -> Supplier:
        row = Supplier(**kwargs)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: Supplier) -> Supplier:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def delete(self, row: Supplier) -> None:
        self.db.delete(row)
        self.db.commit()