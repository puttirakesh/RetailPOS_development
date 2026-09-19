"""RG_Product model – exact RTGW columns."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Product(Base):
    __tablename__ = "RG_Product"
    __table_args__ = {"schema": "dbo"}

    product_id: Mapped[int] = mapped_column(
        "ProductId", Integer, primary_key=True, autoincrement=False
    )
    product_code: Mapped[str] = mapped_column("ProductCode", String(50), nullable=False)
    product_name: Mapped[str] = mapped_column("ProductName", String(200), nullable=False)
    category_id: Mapped[int] = mapped_column("CategoryId", Integer, nullable=False)
    hsn_code: Mapped[Optional[str]] = mapped_column("HSNCode", String(20), nullable=True)
    remarks: Mapped[Optional[str]] = mapped_column("Remarks", String(500), nullable=True)
    is_unique: Mapped[bool] = mapped_column(
        "IsUnique", Boolean, nullable=False, server_default="0", default=False
    )
    is_bulk: Mapped[bool] = mapped_column(
        "IsBulk", Boolean, nullable=False, server_default="0", default=False
    )
    auto_ean_required: Mapped[bool] = mapped_column(
        "AutoEANRequired", Boolean, nullable=False, server_default="0", default=False
    )
    entry_wise_ean_required: Mapped[bool] = mapped_column(
        "EntryWiseEANRequired", Boolean, nullable=False, server_default="0", default=False
    )
    discount_not_applicable: Mapped[bool] = mapped_column(
        "DiscountNotApplicable", Boolean, nullable=False, server_default="0", default=False
    )
    manual_barcode_restriction: Mapped[bool] = mapped_column(
        "ManualBarcodeRestriction", Boolean, nullable=False, server_default="0", default=False
    )
    non_inventory: Mapped[bool] = mapped_column(
        "NonInventory", Boolean, nullable=False, server_default="0", default=False
    )
    is_active: Mapped[bool] = mapped_column(
        "IsActive", Boolean, nullable=False, server_default="1", default=True
    )
    created_date: Mapped[Optional[datetime]] = mapped_column(
        "CreatedDate", DateTime, nullable=True, server_default=func.getdate()
    )
    uom_id: Mapped[Optional[int]] = mapped_column("UOMId", Integer, nullable=True)