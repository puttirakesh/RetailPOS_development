"""Pydantic v2 schemas for Brand CRUD."""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BrandCreate(BaseModel):
    brand_name: str = Field(..., min_length=1, max_length=100)
    margin_percentage: Decimal = Field(default=Decimal("0.00"), max_digits=5, decimal_places=2)
    is_active: bool = True

    @field_validator("brand_name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        name = v.strip().upper()
        if not name:
            raise ValueError("Brand name is required")
        return name

    @field_validator("margin_percentage")
    @classmethod
    def validate_margin(cls, v: Decimal) -> Decimal:
        if v < 0 or v > 999.99:
            raise ValueError("Margin percentage must be between 0 and 999.99")
        return v


class BrandUpdate(BaseModel):
    brand_name: str | None = Field(default=None, min_length=1, max_length=100)
    margin_percentage: Decimal | None = Field(default=None, max_digits=5, decimal_places=2)
    is_active: bool | None = None

    @field_validator("brand_name")
    @classmethod
    def normalize_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        name = v.strip().upper()
        if not name:
            raise ValueError("Brand name cannot be blank")
        return name

    @field_validator("margin_percentage")
    @classmethod
    def validate_margin(cls, v: Decimal | None) -> Decimal | None:
        if v is None:
            return None
        if v < 0 or v > 999.99:
            raise ValueError("Margin percentage must be between 0 and 999.99")
        return v


class BrandRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    brand_id: int
    brand_code: str
    brand_name: str
    margin_percentage: Decimal
    is_active: bool
    created_date: datetime | None = None


class BrandListResponse(BaseModel):
    total: int
    items: list[BrandRead]