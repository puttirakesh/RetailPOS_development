from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryCreate(BaseModel):
    category_code: str | None = Field(default=None, max_length=50)
    category_name: str = Field(..., min_length=1, max_length=100)
    group_id: int = Field(..., gt=0)
    is_active: bool = True

    @field_validator("category_name")
    @classmethod
    def upper_name(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Category name is required")
        return v


class CategoryUpdate(BaseModel):
    category_code: str | None = Field(default=None, max_length=50)
    category_name: str | None = Field(default=None, min_length=1, max_length=100)
    group_id: int | None = Field(default=None, gt=0)
    is_active: bool | None = None


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
    category_code: str | None = None
    category_name: str
    group_id: int
    is_active: bool = True


class CategoryListResponse(BaseModel):
    total: int
    items: list[CategoryRead]