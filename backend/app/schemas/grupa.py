from pydantic import BaseModel
from typing import Optional
from .user import UserResponse

class GrupaBase(BaseModel):
    name: str
    year: Optional[int] = None
    specialization: Optional[str] = None
    leader_id: Optional[int] = None

class GrupaCreate(GrupaBase):
    pass

class GrupaUpdate(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None
    specialization: Optional[str] = None
    leader_id: Optional[int] = None

class GrupaResponse(GrupaBase):
    leader: Optional[UserResponse] = None
    
    class Config:
        orm_mode = True
