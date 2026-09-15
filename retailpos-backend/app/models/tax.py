"""RG_TaxMaster model."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Tax(Base):
    __tablename__ = "RG_TaxMaster"
    __table_args__ = {"schema": "dbo"}

    tax_id: Mapped[int] = mapped_column("TaxId", Integer, primary_key=True, autoincrement=True)
    tax_name: Mapped[str] = mapped_column("TaxName", String(50), nullable=False)
    tax_percentage: Mapped[Decimal] = mapped_column("TaxPercentage", Numeric(5, 2), nullable=False)
    tax_type: Mapped[str] = mapped_column(
        "TaxType", String(20), nullable=False, server_default="GST", default="GST"
    )
    is_active: Mapped[bool] = mapped_column(
        "IsActive", Boolean, nullable=False, server_default="1", default=True
    )
    created_date: Mapped[Optional[datetime]] = mapped_column(
        "CreatedDate", DateTime, nullable=False, server_default=func.getdate()
    )