"""RG_Brand model – matches the live RTGW schema exactly."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Brand(Base):
    """
    Maps 1:1 to dbo.RG_Brand.

    Notes from Phase 0:
    - BrandId is currently a plain INT (not IDENTITY). We treat it as the PK
      and will convert it to IDENTITY(1,1) in a later Alembic migration.
    - Soft-delete is expressed via IsActive (no IsDeleted column exists).
    - No UpdatedAt / CreatedBy / rowversion columns yet.
    """

    __tablename__ = "RG_Brand"
    __table_args__ = {"schema": "dbo"}

    brand_id: Mapped[int] = mapped_column(
        "BrandId",
        Integer,
        primary_key=True,
        autoincrement=False,  # existing table is not IDENTITY yet
    )
    brand_code: Mapped[str] = mapped_column(
        "BrandCode",
        String(20),
        nullable=False,
    )
    brand_name: Mapped[str] = mapped_column(
        "BrandName",
        String(100),
        nullable=False,
    )
    margin_percentage: Mapped[Decimal] = mapped_column(
        "MarginPercentage",
        Numeric(5, 2),
        nullable=False,
        server_default="0",
        default=Decimal("0.00"),
    )
    is_active: Mapped[bool] = mapped_column(
        "IsActive",
        Boolean,
        nullable=False,
        server_default="1",
        default=True,
    )
    created_date: Mapped[Optional[datetime]] = mapped_column(
        "CreatedDate",
        DateTime,
        nullable=False,
        server_default=func.getdate(),
    )

    def __repr__(self) -> str:
        return (
            f"<Brand id={self.brand_id} "
            f"code={self.brand_code!r} name={self.brand_name!r}>"
        )