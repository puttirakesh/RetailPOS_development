"""RG_UOM model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Uom(Base):
    __tablename__ = "RG_UOM"
    __table_args__ = {"schema": "dbo"}

    uom_id: Mapped[int] = mapped_column("UOMId", Integer, primary_key=True, autoincrement=False)
    uom_code: Mapped[str] = mapped_column("UOMCode", String(10), nullable=False)
    uom_name: Mapped[str] = mapped_column("UOMName", String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        "IsActive", Boolean, nullable=False, server_default="1", default=True
    )
    created_date: Mapped[Optional[datetime]] = mapped_column(
        "CreatedDate", DateTime, nullable=False, server_default=func.getdate()
    )