"""UOM repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.uom import Uom


class UomRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self, *, active_only: bool = True, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> list[Uom]:
        stmt = select(Uom).order_by(Uom.uom_id)
        if active_only:
            stmt = stmt.where(Uom.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where((Uom.uom_name.ilike(term)) | (Uom.uom_code.ilike(term)))
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(self, *, active_only: bool = True, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(Uom)
        if active_only:
            stmt = stmt.where(Uom.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where((Uom.uom_name.ilike(term)) | (Uom.uom_code.ilike(term)))
        return self.db.scalar(stmt) or 0

    def get_by_id(self, uom_id: int) -> Uom | None:
        return self.db.get(Uom, uom_id)

    def get_by_code(self, code: str, *, exclude_id: int | None = None) -> Uom | None:
        stmt = select(Uom).where(Uom.uom_code == code)
        if exclude_id is not None:
            stmt = stmt.where(Uom.uom_id != exclude_id)
        return self.db.scalars(stmt).first()

    def get_by_name(self, name: str, *, exclude_id: int | None = None) -> Uom | None:
        stmt = select(Uom).where(Uom.uom_name == name)
        if exclude_id is not None:
            stmt = stmt.where(Uom.uom_id != exclude_id)
        return self.db.scalars(stmt).first()

    def next_id(self) -> int:
        return int(self.db.scalar(select(func.max(Uom.uom_id))) or 0) + 1

    def create(self, *, uom_id: int, uom_code: str, uom_name: str, is_active: bool) -> Uom:
        row = Uom(uom_id=uom_id, uom_code=uom_code, uom_name=uom_name, is_active=is_active)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: Uom) -> Uom:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def soft_delete(self, row: Uom) -> Uom:
        row.is_active = False
        return self.update(row)