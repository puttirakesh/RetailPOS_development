"""State repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.state import State


class StateRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(
        self, *, active_only: bool = True, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> list[State]:
        stmt = select(State).order_by(State.state_id)
        if active_only:
            stmt = stmt.where(State.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where((State.state_name.ilike(term)) | (State.state_code.ilike(term)))
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(self, *, active_only: bool = True, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(State)
        if active_only:
            stmt = stmt.where(State.is_active == True)  # noqa: E712
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where((State.state_name.ilike(term)) | (State.state_code.ilike(term)))
        return self.db.scalar(stmt) or 0

    def get_by_id(self, state_id: int) -> State | None:
        return self.db.get(State, state_id)

    def get_by_code(self, code: str, *, exclude_id: int | None = None) -> State | None:
        stmt = select(State).where(State.state_code == code)
        if exclude_id is not None:
            stmt = stmt.where(State.state_id != exclude_id)
        return self.db.scalars(stmt).first()

    def next_id(self) -> int:
        return int(self.db.scalar(select(func.max(State.state_id))) or 0) + 1

    def create(self, **kwargs) -> State:
        row = State(**kwargs)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: State) -> State:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def soft_delete(self, row: State) -> State:
        row.is_active = False
        return self.update(row)