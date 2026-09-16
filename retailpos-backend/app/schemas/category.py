from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryCreate(BaseModel):
    category_code: str = Field(..., min_length=1, max_length=50)
    category_name: str = Field(..., min_length=1, max_length=100)
    group_id: int = Field(..., gt=0)
    is_active: bool = True

    @field_validator("category_code", "category_name")
    @classmethod
    def upper_strip(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Required")
        return v


class CategoryUpdate(BaseModel):
    category_code: str | None = Field(default=None, min_length=1, max_length=50)
    category_name: str | None = Field(default=None, min_length=1, max_length=100)
    group_id: int | None = Field(default=None, gt=0)
    is_active: bool | None = None

    @field_validator("category_code", "category_name")
    @classmethod
    def upper_strip(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        if not v:
            raise ValueError("Cannot be blank")
        return v


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    category_id: int
    category_code: str
    category_name: str
    group_id: int
    is_active: bool
    created_date: datetime | None = None


class CategoryListResponse(BaseModel):
    total: int
    items: list[CategoryRead]