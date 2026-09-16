from pydantic import BaseModel, ConfigDict, Field, field_validator


class GroupCreate(BaseModel):
    group_code: str = Field(..., min_length=1, max_length=50)
    group_name: str = Field(..., min_length=1, max_length=100)
    slab_req: bool = False
    tax_id: int = 0
    b_value: float = 0.0
    b_tax_id: int = 0
    a_value: float = 0.0

    @field_validator("group_code", "group_name")
    @classmethod
    def upper_strip(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Required")
        return v


class GroupUpdate(BaseModel):
    group_code: str | None = Field(default=None, min_length=1, max_length=50)
    group_name: str | None = Field(default=None, min_length=1, max_length=100)
    slab_req: bool | None = None
    tax_id: int | None = None
    b_value: float | None = None
    b_tax_id: int | None = None
    a_value: float | None = None

    @field_validator("group_code", "group_name")
    @classmethod
    def upper_strip(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        if not v:
            raise ValueError("Cannot be blank")
        return v


class GroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    group_id: int
    group_code: str
    group_name: str
    slab_req: bool
    tax_id: int
    b_value: float
    b_tax_id: int
    a_value: float


class GroupListResponse(BaseModel):
    total: int
    items: list[GroupRead]