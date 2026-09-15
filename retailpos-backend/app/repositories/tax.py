"""TaxMaster repository. TaxId is IDENTITY – no MAX+1."""

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.tax import Tax


class TaxRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self, *, active_only: bool = True, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> list[Tax]:
        stmt = select(Tax).order_by(Tax.tax_id)
        if active_only:
            stmt = stmt.where(Tax.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(Tax.tax_name.ilike(term))
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(self, *, active_only: bool = True, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(Tax)
        if active_only:
            stmt = stmt.where(Tax.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(Tax.tax_name.ilike(term))
        return self.db.scalar(stmt) or 0

    def get_by_id(self, tax_id: int) -> Tax | None:
        return self.db.get(Tax, tax_id)

    def get_by_name(self, name: str, *, exclude_id: int | None = None) -> Tax | None:
        stmt = select(Tax).where(Tax.tax_name == name)
        if exclude_id is not None:
            stmt = stmt.where(Tax.tax_id != exclude_id)
        return self.db.scalars(stmt).first()

    def create(
        self,
        *,
        tax_name: str,
        tax_percentage: Decimal,
        tax_type: str,
        is_active: bool,
    ) -> Tax:
        row = Tax(
            tax_name=tax_name,
            tax_percentage=tax_percentage,
            tax_type=tax_type,
            is_active=is_active,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: Tax) -> Tax:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def soft_delete(self, row: Tax) -> Tax:
        row.is_active = False
        return self.update(row)