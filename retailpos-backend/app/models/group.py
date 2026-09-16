"""RG_Group model."""

from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Group(Base):
    __tablename__ = "RG_Group"
    __table_args__ = {"schema": "dbo"}

    group_id: Mapped[int] = mapped_column("GroupId", Integer, primary_key=True, autoincrement=False)
    group_code: Mapped[str] = mapped_column("GroupCode", String(50), nullable=False)
    group_name: Mapped[str] = mapped_column("GroupName", String(100), nullable=False)
    slab_req: Mapped[bool] = mapped_column(
        "SlabReq", Boolean, nullable=False, server_default="0", default=False
    )
    tax_id: Mapped[int] = mapped_column("TaxId", Integer, nullable=False, default=0)
    b_value: Mapped[float] = mapped_column("BValue", Float, nullable=False, default=0.0)
    b_tax_id: Mapped[int] = mapped_column("BTaxId", Integer, nullable=False, default=0)
    a_value: Mapped[float] = mapped_column("AValue", Float, nullable=False, default=0.0)