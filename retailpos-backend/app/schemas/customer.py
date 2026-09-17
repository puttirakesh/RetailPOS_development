from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CustomerCreate(BaseModel):
    customer_code: str | None = Field(default=None, max_length=20)
    customer_name: str = Field(..., min_length=1, max_length=150)
    mobile_no: str | None = Field(default=None, max_length=15)
    address: str | None = Field(default=None, max_length=300)
    city_id: int | None = None
    state_id: int = Field(..., gt=0)
    gst_no: str | None = Field(default=None, max_length=20)
    credit_days: int = Field(default=0, ge=0)
    credit_limit: Decimal = Field(default=Decimal("0.00"), max_digits=18, decimal_places=2)
    opening_balance: Decimal = Field(default=Decimal("0.00"), max_digits=18, decimal_places=2)
    ledger_required: bool = False
    email_id: str | None = Field(default=None, max_length=100)
    is_active: bool = True
    discount_percentage: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)
    discount_amount: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)

    @field_validator("customer_name")
    @classmethod
    def upper_name(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Customer name is required")
        return v


class CustomerUpdate(BaseModel):
    customer_code: str | None = Field(default=None, max_length=20)
    customer_name: str | None = Field(default=None, min_length=1, max_length=150)
    mobile_no: str | None = Field(default=None, max_length=15)
    address: str | None = Field(default=None, max_length=300)
    city_id: int | None = None
    state_id: int | None = Field(default=None, gt=0)
    gst_no: str | None = Field(default=None, max_length=20)
    credit_days: int | None = Field(default=None, ge=0)
    credit_limit: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)
    opening_balance: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)
    ledger_required: bool | None = None
    email_id: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None
    discount_percentage: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)
    discount_amount: Decimal | None = Field(default=None, max_digits=18, decimal_places=2)

    @field_validator("customer_name")
    @classmethod
    def upper_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        if not v:
            raise ValueError("Cannot be blank")
        return v


class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    customer_id: int
    customer_code: str | None
    customer_name: str
    mobile_no: str | None
    address: str | None
    city_id: int | None
    state_id: int
    gst_no: str | None
    credit_days: int
    credit_limit: Decimal
    opening_balance: Decimal
    ledger_required: bool
    email_id: str | None
    is_active: bool
    created_date: datetime | None = None
    discount_percentage: Decimal | None = None
    discount_amount: Decimal | None = None


class CustomerListResponse(BaseModel):
    total: int
    items: list[CustomerRead]