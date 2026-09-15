"""RG_User model – matches the live RTGW schema (Password widened for bcrypt)."""

from typing import Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """
    Maps 1:1 to dbo.RG_User.

    Run once in SSMS if Password is still VARCHAR(50):
        ALTER TABLE dbo.RG_User ALTER COLUMN [Password] VARCHAR(100) NOT NULL;
    """

    __tablename__ = "RG_User"
    __table_args__ = {"schema": "dbo"}

    user_id: Mapped[int] = mapped_column(
        "UserId", Integer, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        "UserName", String(50), nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(
        "Password", String(100), nullable=False
    )
    is_admin: Mapped[Optional[bool]] = mapped_column(
        "IsAdmin", Boolean, nullable=True, server_default="0", default=False
    )
    is_active: Mapped[bool] = mapped_column(
        "IsActive", Boolean, nullable=False, server_default="1", default=True
    )

    @property
    def role(self) -> str:
        if self.is_admin:
            return "admin"
        return "cashier"

    def __repr__(self) -> str:
        return f"<User id={self.user_id} username={self.username!r} role={self.role}>"