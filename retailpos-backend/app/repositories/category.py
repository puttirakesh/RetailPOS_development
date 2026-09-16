"""Category repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self,
        *,
        active_only: bool = True,
        group_id: int | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Category]:
        stmt = select(Category).order_by(Category.category_id)
        if active_only:
            stmt = stmt.where(Category.is_active == True)  # noqa: E712
        if group_id is not None:
            stmt = stmt.where(Category.group_id == group_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                (Category.category_name.ilike(term)) | (Category.category_code.ilike(term))
            )
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(
        self,
        *,
        active_only: bool = True,
        group_id: int | None = None,
        search: str | None = None,
    ) -> int:
        stmt = select(func.count()).select_from(Category)
        if active_only:
            stmt = stmt.where(Category.is_active == True)  # noqa: E712
        if group_id is not None:
            stmt = stmt.where(Category.group_id == group_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(
                (Category.category_name.ilike(term)) | (Category.category_code.ilike(term))
            )
        return self.db.scalar(stmt) or 0

    def get_by_id(self, category_id: int) -> Category | None:
        return self.db.get(Category, category_id)

    def next_id(self) -> int:
        return int(self.db.scalar(select(func.max(Category.category_id))) or 0) + 1

    def create(self, **kwargs) -> Category:
        row = Category(**kwargs)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: Category) -> Category:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def soft_delete(self, row: Category) -> Category:
        row.is_active = False
        return self.update(row)