from pydantic import BaseModel, ConfigDict, Field, field_validator


class AgentCreate(BaseModel):
    agent_name: str = Field(..., min_length=1, max_length=100)
    address: str = Field(default="", max_length=500)
    mobile: int = Field(default=0, ge=0)
    city_id: int = Field(default=0, ge=0)

    @field_validator("agent_name")
    @classmethod
    def upper_name(cls, v: str) -> str:
        v = v.strip().upper()
        if not v:
            raise ValueError("Agent name is required")
        return v


class AgentUpdate(BaseModel):
    agent_name: str | None = Field(default=None, min_length=1, max_length=100)
    address: str | None = Field(default=None, max_length=500)
    mobile: int | None = Field(default=None, ge=0)
    city_id: int | None = Field(default=None, ge=0)

    @field_validator("agent_name")
    @classmethod
    def upper_name(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip().upper()
        if not v:
            raise ValueError("Cannot be blank")
        return v


class AgentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    agent_id: int
    agent_name: str
    address: str
    mobile: int
    city_id: int


class AgentListResponse(BaseModel):
    total: int
    items: list[AgentRead]