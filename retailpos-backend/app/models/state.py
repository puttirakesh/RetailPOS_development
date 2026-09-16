"""RG_State model."""

from sqlalchemy import Boolean, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class State(Base):
    __tablename__ = "RG_State"
    __table_args__ = {"schema": "dbo"}

    state_id: Mapped[int] = mapped_column("StateId", Integer, primary_key=True, autoincrement=False)
    state_code: Mapped[str] = mapped_column("StateCode", String(2), nullable=False)
    state_name: Mapped[str] = mapped_column("StateName", String(100), nullable=False)
    state_type: Mapped[int] = mapped_column("StateType", SmallInteger, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(
        "IsActive", Boolean, nullable=False, server_default="1", default=True
    )