"""Agent CRUD – JWT required."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.agent import AgentCreate, AgentListResponse, AgentRead, AgentUpdate
from app.services.agent import AgentService

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("", response_model=AgentListResponse)
def list_agents(
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
    search: str | None = Query(None, max_length=100),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> AgentListResponse:
    return AgentService(db).list_items(search=search, skip=skip, limit=limit)


@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(
    agent_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> AgentRead:
    return AgentService(db).get(agent_id)


@router.post("", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
def create_agent(
    body: AgentCreate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> AgentRead:
    return AgentService(db).create(body)


@router.put("/{agent_id}", response_model=AgentRead)
def update_agent(
    agent_id: int,
    body: AgentUpdate,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> AgentRead:
    return AgentService(db).update(agent_id, body)


@router.delete("/{agent_id}")
def delete_agent(
    agent_id: int,
    db: Annotated[Session, Depends(get_db)],
    _user: Annotated[User, Depends(get_current_user)],
) -> dict[str, str]:
    return AgentService(db).delete(agent_id)