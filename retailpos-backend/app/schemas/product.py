"""Pydantic schemas for Product."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    product_code: str | None = Field(default=None, max_length=50)
    product_name: str = Field(..., min_length=1, max_length=200)
    category_id: int = Field(..., gt=0)
    hsn_code: str | None = Field(default=None, max_length=20)
    remarks: str | None = Field(default=None, max_length=500)
    is_unique: bool = False
    is_bulk: bool = False
    auto_ean_required: bool = False
    entry_wise_ean_required: bool = False
    discount_not_applicable: bool = False
    manual_barcode_restriction: bool = False
    non_inventory: bool = False
    uom_id: int | None = None
    is_active: bool = True

    @field_validator("product_name")
    @classmethod
    def upper_name(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Product name is required")
        return v

    @field_validator("product_code", "hsn_code")
    @classmethod
    def upper_optional(cls, v: str | None) -> str | None:
        if v is None or not str(v).strip():
            return None
        return str(v).strip().upper()


class ProductUpdate(BaseModel):
    product_code: str | None = Field(default=None, max_length=50)
    product_name: str | None = Field(default=None, min_length=1, max_length=200)
    category_id: int | None = Field(default=None, gt=0)
    hsn_code: str | None = Field(default=None, max_length=20)
    remarks: str | None = Field(default=None, max_length=500)
    is_unique: bool | None = None
    is_bulk: bool | None = None
    auto_ean_required: bool | None = None
    entry_wise_ean_required: bool | None = None
    discount_not_applicable: bool | None = None
    manual_barcode_restriction: bool | None = None
    non_inventory: bool | None = None
    uom_id: int | None = None
    is_active: bool | None = None

    @field_validator("product_name")
    @classmethod
    def upper_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        if not v:
            raise ValueError("Cannot be blank")
        return v


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    product_code: str
    product_name: str
    category_id: int
    hsn_code: str | None = None
    remarks: str | None = None
    is_unique: bool
    is_bulk: bool
    auto_ean_required: bool
    entry_wise_ean_required: bool
    discount_not_applicable: bool
    manual_barcode_restriction: bool
    non_inventory: bool
    uom_id: int | None = None
    is_active: bool = True
    created_date: datetime | None = None


class ProductListResponse(BaseModel):
    total: int
    items: list[ProductRead]