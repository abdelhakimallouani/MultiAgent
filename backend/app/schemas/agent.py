from pydantic import BaseModel
from typing import Optional


class AgentCreate(BaseModel):
    name: str
    role: str
    description: str
    system_prompt: str
    model: str
    temperature: float = 0.7


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    is_active: Optional[bool] = None


class AgentResponse(BaseModel):
    id: int
    name: str
    role: str
    description: str
    system_prompt: str
    model: str
    temperature: float
    is_active: bool

    class Config:
        from_attributes = True