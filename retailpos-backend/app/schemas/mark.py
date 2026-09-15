"""Pydantic schemas for Mark."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MarkCreate(BaseModel):
    mark_code: str | None = Field(default=None, max_length=20)
    mark_amount: Decimal = Field(default=Decimal("0.00"), max_digits=18, decimal_places=2)
    is_active: bool = True

    @field_validator("mark_code")
    @classmethod
    def upper_code(cls, v: str | None) -> str | None:
        if v is None or not v.strip():
            return None
        return v.strip().upper()

    @field_validator("mark_amount")
    @classmethod
    def non_negative(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Mark amount cannot be negative")
        return v


class MarkUpdate(BaseModel):
    mark_code: str | None = Field(default=None, max_length=20)
    mark_amount: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)
    is_active: bool | None = None

    @field_validator("mark_code")
    @classmethod
    def upper_code(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if not v.strip():
            return None
        return v.strip().upper()

    @field_validator("mark_amount")
    @classmethod
    def non_negative(cls, v: Decimal | None) -> Decimal | None:
        if v is not None and v < 0:
            raise ValueError("Mark amount cannot be negative")
        return v


class MarkRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mark_id: int
    mark_code: str | None
    mark_amount: Decimal
    is_active: bool
    created_date: datetime | None = None


class MarkListResponse(BaseModel):
    total: int
    items: list[MarkRead]