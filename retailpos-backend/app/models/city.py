"""RG_City model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class City(Base):
    __tablename__ = "RG_City"
    __table_args__ = {"schema": "dbo"}

    city_id: Mapped[int] = mapped_column("CityId", Integer, primary_key=True, autoincrement=False)
    city_code: Mapped[str] = mapped_column("CityCode", String(10), nullable=False)
    city_name: Mapped[str] = mapped_column("CityName", String(100), nullable=False)
    state_id: Mapped[int] = mapped_column("StateId", Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        "IsActive", Boolean, nullable=False, server_default="1", default=True
    )
    created_date: Mapped[datetime | None] = mapped_column(
        "CreatedDate", DateTime, nullable=False, server_default=func.getdate()
    )