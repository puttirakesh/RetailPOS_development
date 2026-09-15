"""Mark repository."""

from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.mark import Mark


class MarkRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self, *, active_only: bool = True, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> list[Mark]:
        stmt = select(Mark).order_by(Mark.mark_id)
        if active_only:
            stmt = stmt.where(Mark.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(Mark.mark_code.ilike(term))
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(self, *, active_only: bool = True, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(Mark)
        if active_only:
            stmt = stmt.where(Mark.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(Mark.mark_code.ilike(term))
        return self.db.scalar(stmt) or 0

    def get_by_id(self, mark_id: int) -> Mark | None:
        return self.db.get(Mark, mark_id)

    def next_id(self) -> int:
        return int(self.db.scalar(select(func.max(Mark.mark_id))) or 0) + 1

    def create(
        self,
        *,
        mark_id: int,
        mark_code: str | None,
        mark_amount: Decimal,
        is_active: bool,
    ) -> Mark:
        row = Mark(
            mark_id=mark_id,
            mark_code=mark_code or str(mark_id),
            mark_amount=mark_amount,
            is_active=is_active,
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: Mark) -> Mark:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def soft_delete(self, row: Mark) -> Mark:
        row.is_active = False
        return self.update(row)