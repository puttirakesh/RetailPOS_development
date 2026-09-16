from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CityCreate(BaseModel):
    city_code: str = Field(..., min_length=1, max_length=10)
    city_name: str = Field(..., min_length=1, max_length=100)
    state_id: int = Field(..., gt=0)
    is_active: bool = True

    @field_validator("city_code", "city_name")
    @classmethod
    def upper_strip(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Required")
        return v


class CityUpdate(BaseModel):
    city_code: str | None = Field(default=None, min_length=1, max_length=10)
    city_name: str | None = Field(default=None, min_length=1, max_length=100)
    state_id: int | None = Field(default=None, gt=0)
    is_active: bool | None = None

    @field_validator("city_code", "city_name")
    @classmethod
    def upper_strip(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        if not v:
            raise ValueError("Cannot be blank")
        return v


class CityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    city_id: int
    city_code: str
    city_name: str
    state_id: int
    is_active: bool
    created_date: datetime | None = None


class CityListResponse(BaseModel):
    total: int
    items: list[CityRead]