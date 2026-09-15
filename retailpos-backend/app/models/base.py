"""SQLAlchemy 2.0 declarative base and common mixins."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TimestampMixin:
    """CreatedDate is already present on most RTW tables as `CreatedDate`."""

    created_date: Mapped[datetime] = mapped_column(
        "CreatedDate",
        DateTime,
        server_default=func.getdate(),
        nullable=False,
    )


class ActiveMixin:
    """Soft-active flag used across all master tables (IsActive BIT)."""

    is_active: Mapped[bool] = mapped_column(
        "IsActive",
        Boolean,
        nullable=False,
        server_default="1",
        default=True,
    )