"""RG_Agent model."""

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Agent(Base):
    __tablename__ = "RG_Agent"
    __table_args__ = {"schema": "dbo"}

    agent_id: Mapped[int] = mapped_column("AgentId", Integer, primary_key=True, autoincrement=False)
    agent_name: Mapped[str] = mapped_column("AgentName", String(100), nullable=False)
    address: Mapped[str] = mapped_column("Address", String(500), nullable=False, default="")
    mobile: Mapped[int] = mapped_column("Mobile", BigInteger, nullable=False, default=0)
    city_id: Mapped[int] = mapped_column("CityId", Integer, nullable=False, default=0)