from pydantic import BaseModel, ConfigDict, Field, field_validator


class StateCreate(BaseModel):
    state_code: str = Field(..., min_length=1, max_length=2)
    state_name: str = Field(..., min_length=1, max_length=100)
    state_type: int = Field(default=0, ge=0, le=255)
    is_active: bool = True

    @field_validator("state_code", "state_name")
    @classmethod
    def upper_strip(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Required")
        return v


class StateUpdate(BaseModel):
    state_code: str | None = Field(default=None, min_length=1, max_length=2)
    state_name: str | None = Field(default=None, min_length=1, max_length=100)
    state_type: int | None = Field(default=None, ge=0, le=255)
    is_active: bool | None = None

    @field_validator("state_code", "state_name")
    @classmethod
    def upper_strip(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        if not v:
            raise ValueError("Cannot be blank")
        return v


class StateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    state_id: int
    state_code: str
    state_name: str
    state_type: int
    is_active: bool


class StateListResponse(BaseModel):
    total: int
    items: list[StateRead]