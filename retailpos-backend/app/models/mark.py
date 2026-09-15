"""RG_Mark model."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Mark(Base):
    __tablename__ = "RG_Mark"
    __table_args__ = {"schema": "dbo"}

    mark_id: Mapped[int] = mapped_column("MarkId", Integer, primary_key=True, autoincrement=False)
    mark_code: Mapped[Optional[str]] = mapped_column("MarkCode", String(20), nullable=True)
    mark_amount: Mapped[Decimal] = mapped_column(
        "MarkAmount", Numeric(18, 2), nullable=False, server_default="0", default=Decimal("0.00")
    )
    is_active: Mapped[bool] = mapped_column(
        "IsActive", Boolean, nullable=False, server_default="1", default=True
    )
    created_date: Mapped[Optional[datetime]] = mapped_column(
        "CreatedDate", DateTime, nullable=False, server_default=func.getdate()
    )