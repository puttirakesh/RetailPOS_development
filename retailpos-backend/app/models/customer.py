"""RG_Customer model – matches live RTGW columns."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Customer(Base):
    __tablename__ = "RG_Customer"
    __table_args__ = {"schema": "dbo"}

    customer_id: Mapped[int] = mapped_column(
        "CustomerId", Integer, primary_key=True, autoincrement=False
    )
    customer_code: Mapped[Optional[str]] = mapped_column("CustomerCode", String(20), nullable=True)
    customer_name: Mapped[str] = mapped_column("CustomerName", String(150), nullable=False)
    mobile_no: Mapped[Optional[str]] = mapped_column("MobileNo", String(15), nullable=True)
    address: Mapped[Optional[str]] = mapped_column("Address", String(300), nullable=True)
    city_id: Mapped[Optional[int]] = mapped_column("CityId", Integer, nullable=True)
    state_id: Mapped[int] = mapped_column("StateId", Integer, nullable=False)
    gst_no: Mapped[Optional[str]] = mapped_column("GSTNo", String(20), nullable=True)
    credit_days: Mapped[int] = mapped_column("CreditDays", Integer, nullable=False, default=0)
    credit_limit: Mapped[Decimal] = mapped_column(
        "CreditLimit", Numeric(18, 2), nullable=False, default=Decimal("0.00")
    )
    opening_balance: Mapped[Decimal] = mapped_column(
        "OpeningBalance", Numeric(18, 2), nullable=False, default=Decimal("0.00")
    )
    ledger_required: Mapped[bool] = mapped_column(
        "LedgerRequired", Boolean, nullable=False, default=False
    )
    email_id: Mapped[Optional[str]] = mapped_column("EmailId", String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        "IsActive", Boolean, nullable=False, server_default="1", default=True
    )
    created_date: Mapped[Optional[datetime]] = mapped_column(
        "CreatedDate", DateTime, nullable=False, server_default=func.getdate()
    )
    discount_percentage: Mapped[Optional[Decimal]] = mapped_column(
        "DiscountPercentage", Numeric(18, 2), nullable=True
    )
    discount_amount: Mapped[Optional[Decimal]] = mapped_column(
        "DiscountAmount", Numeric(18, 2), nullable=True
    )