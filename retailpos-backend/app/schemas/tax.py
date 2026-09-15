"""Pydantic schemas for TaxMaster."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaxCreate(BaseModel):
    tax_name: str = Field(..., min_length=1, max_length=50)
    tax_percentage: Decimal = Field(..., max_digits=5, decimal_places=2)
    tax_type: str = Field(default="GST", max_length=20)
    is_active: bool = True

    @field_validator("tax_name")
    @classmethod
    def upper_name(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Tax name is required")
        return v

    @field_validator("tax_percentage")
    @classmethod
    def valid_pct(cls, v: Decimal) -> Decimal:
        if v < 0 or v > 100:
            raise ValueError("Tax percentage must be between 0 and 100")
        return v

    @field_validator("tax_type")
    @classmethod
    def upper_type(cls, v: str) -> str:
        return v.strip().upper() or "GST"


class TaxUpdate(BaseModel):
    tax_name: str | None = Field(default=None, min_length=1, max_length=50)
    tax_percentage: Decimal | None = Field(default=None, max_digits=5, decimal_places=2)
    tax_type: str | None = Field(default=None, max_length=20)
    is_active: bool | None = None

    @field_validator("tax_name")
    @classmethod
    def upper_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        if not v:
            raise ValueError("Tax name cannot be blank")
        return v

    @field_validator("tax_percentage")
    @classmethod
    def valid_pct(cls, v: Decimal | None) -> Decimal | None:
        if v is not None and (v < 0 or v > 100):
            raise ValueError("Tax percentage must be between 0 and 100")
        return v

    @field_validator("tax_type")
    @classmethod
    def upper_type(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return v.strip().upper() or "GST"


class TaxRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tax_id: int
    tax_name: str
    tax_percentage: Decimal
    tax_type: str
    is_active: bool
    created_date: datetime | None = None


class TaxListResponse(BaseModel):
    total: int
    items: list[TaxRead]