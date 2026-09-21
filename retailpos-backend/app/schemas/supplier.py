from pydantic import BaseModel, ConfigDict, Field, field_validator


class SupplierCreate(BaseModel):
    supplier_code: str | None = Field(default=None, max_length=20)
    supplier_name: str = Field(..., min_length=1, max_length=150)
    mobile_no: str | None = Field(default=None, max_length=15)
    address: str | None = Field(default=None, max_length=300)
    city_id: int | None = None
    state_id: int | None = None
    gst_no: str = Field(default="", max_length=20)

    @field_validator("supplier_name")
    @classmethod
    def upper_name(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Supplier name is required")
        return v

    @field_validator("gst_no", mode="before")
    @classmethod
    def gst_default(cls, v):
        if v is None:
            return ""
        return str(v).strip().upper()


class SupplierUpdate(BaseModel):
    supplier_code: str | None = Field(default=None, max_length=20)
    supplier_name: str | None = Field(default=None, min_length=1, max_length=150)
    mobile_no: str | None = Field(default=None, max_length=15)
    address: str | None = Field(default=None, max_length=300)
    city_id: int | None = None
    state_id: int | None = None
    gst_no: str | None = Field(default=None, max_length=20)


class SupplierRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    supplier_id: int
    supplier_code: str | None = None
    supplier_name: str
    mobile_no: str | None = None
    address: str | None = None
    city_id: int | None = None
    state_id: int | None = None
    gst_no: str = ""


class SupplierListResponse(BaseModel):
    total: int
    items: list[SupplierRead]