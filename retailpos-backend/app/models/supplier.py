"""RG_Supplier model."""

from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Supplier(Base):
    __tablename__ = "RG_Supplier"
    __table_args__ = {"schema": "dbo"}

    supplier_id: Mapped[int] = mapped_column(
        "SupplierId", Integer, primary_key=True, autoincrement=False
    )
    supplier_code: Mapped[Optional[str]] = mapped_column("SupplierCode", String(20), nullable=True)
    supplier_name: Mapped[str] = mapped_column("SupplierName", String(150), nullable=False)
    mobile_no: Mapped[Optional[str]] = mapped_column("MobileNo", String(15), nullable=True)
    address: Mapped[Optional[str]] = mapped_column("Address", String(300), nullable=True)
    city_id: Mapped[Optional[int]] = mapped_column("CityId", Integer, nullable=True)
    state_id: Mapped[Optional[int]] = mapped_column("StateId", Integer, nullable=True)
    gst_no: Mapped[str] = mapped_column("GSTNo", String(20), nullable=False, default="")