"""Agent repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.agent import Agent


class AgentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, *, search: str | None = None, skip: int = 0, limit: int = 50) -> list[Agent]:
        stmt = select(Agent).order_by(Agent.agent_id)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(Agent.agent_name.ilike(term))
        return list(self.db.scalars(stmt.offset(skip).limit(limit)).all())

    def count(self, *, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(Agent)
        if search:
            term = f"%{search.strip()}%"
            stmt = stmt.where(Agent.agent_name.ilike(term))
        return self.db.scalar(stmt) or 0

    def get_by_id(self, agent_id: int) -> Agent | None:
        return self.db.get(Agent, agent_id)

    def next_id(self) -> int:
        return int(self.db.scalar(select(func.max(Agent.agent_id))) or 0) + 1

    def create(self, **kwargs) -> Agent:
        row = Agent(**kwargs)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def update(self, row: Agent) -> Agent:
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

    def delete(self, row: Agent) -> None:
        self.db.delete(row)
        self.db.commit()