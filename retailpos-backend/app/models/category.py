"""RG_Category – only columns that exist in RTGW."""

from typing import Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Category(Base):
    __tablename__ = "RG_Category"
    __table_args__ = {"schema": "dbo"}

    category_id: Mapped[int] = mapped_column(
        "CategoryId", Integer, primary_key=True, autoincrement=False
    )
    category_code: Mapped[Optional[str]] = mapped_column(
        "CategoryCode", String(50), nullable=True
    )
    category_name: Mapped[str] = mapped_column(
        "CategoryName", String(100), nullable=False
    )
    group_id: Mapped[int] = mapped_column("GroupId", Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        "IsActive", Boolean, nullable=False, server_default="1", default=True
    )