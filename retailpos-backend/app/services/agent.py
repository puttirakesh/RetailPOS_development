"""Agent business logic."""

from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.agent import AgentRepository
from app.schemas.agent import AgentCreate, AgentListResponse, AgentRead, AgentUpdate


class AgentService:
    def __init__(self, db: Session) -> None:
        self.repo = AgentRepository(db)

    def list_items(
        self, *, search: str | None = None, skip: int = 0, limit: int = 50
    ) -> AgentListResponse:
        items = self.repo.get_all(search=search, skip=skip, limit=limit)
        total = self.repo.count(search=search)
        return AgentListResponse(total=total, items=[AgentRead.model_validate(i) for i in items])

    def get(self, agent_id: int) -> AgentRead:
        row = self.repo.get_by_id(agent_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        return AgentRead.model_validate(row)

    def create(self, payload: AgentCreate) -> AgentRead:
        agent_id = self.repo.next_id()
        row = self.repo.create(
            agent_id=agent_id,
            agent_name=payload.agent_name,
            address=payload.address or "",
            mobile=payload.mobile,
            city_id=payload.city_id,
        )
        return AgentRead.model_validate(row)

    def update(self, agent_id: int, payload: AgentUpdate) -> AgentRead:
        row = self.repo.get_by_id(agent_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise HTTPException(status_code=422, detail="No fields to update")
        for k, v in data.items():
            setattr(row, k, v)
        return AgentRead.model_validate(self.repo.update(row))

    def delete(self, agent_id: int) -> dict[str, str]:
        row = self.repo.get_by_id(agent_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        self.repo.delete(row)
        return {"detail": f"Agent {agent_id} deleted"}