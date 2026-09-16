"""RG_Category model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Category(Base):
    __tablename__ = "RG_Category"
    __table_args__ = {"schema": "dbo"}

    category_id: Mapped[int] = mapped_column(
        "CategoryId", Integer, primary_key=True, autoincrement=False
    )
    category_code: Mapped[str] = mapped_column("CategoryCode", String(50), nullable=False)
    category_name: Mapped[str] = mapped_column("CategoryName", String(100), nullable=False)
    group_id: Mapped[int] = mapped_column("GroupId", Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        "IsActive", Boolean, nullable=False, server_default="1", default=True
    )
    created_date: Mapped[datetime | None] = mapped_column(
        "CreatedDate", DateTime, nullable=True, server_default=func.getdate()
    )