"""Group repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.group import Group


class GroupRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self, *, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> list[Group]:
        stmt = select(Group).order_by(Group.group_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where((Group.group_name.ilike(term)) | (Group.group_code.ilike(term)))
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(self, *, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(Group)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where((Group.group_name.ilike(term)) | (Group.group_code.ilike(term)))
        return self.db.scalar(stmt) or 0

    def get_by_id(self, group_id: int) -> Group | None:
        return self.db.get(Group, group_id)

    def get_by_code(self, code: str, *, exclude_id: int | None = None) -> Group | None:
        stmt = select(Group).where(Group.group_code == code)
        if exclude_id is not None:
            stmt = stmt.where(Group.group_id != exclude_id)
        return self.db.scalars(stmt).first()

    def next_id(self) -> int:
        return int(self.db.scalar(select(func.max(Group.group_id))) or 0) + 1

    def create(self, **kwargs) -> Group:
        row = Group(**kwargs)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: Group) -> Group:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def delete(self, row: Group) -> None:
        self.db.delete(row)
        self.db.commit()