"""Pydantic schemas for UOM."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UomCreate(BaseModel):
    uom_code: str = Field(..., min_length=1, max_length=10)
    uom_name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True

    @field_validator("uom_code", "uom_name")
    @classmethod
    def upper_strip(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Value is required")
        return v


class UomUpdate(BaseModel):
    uom_code: str | None = Field(default=None, min_length=1, max_length=10)
    uom_name: str | None = Field(default=None, min_length=1, max_length=100)
    is_active: bool | None = None

    @field_validator("uom_code", "uom_name")
    @classmethod
    def upper_strip(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        if not v:
            raise ValueError("Value cannot be blank")
        return v


class UomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uom_id: int
    uom_code: str
    uom_name: str
    is_active: bool
    created_date: datetime | None = None


class UomListResponse(BaseModel):
    total: int
    items: list[UomRead]