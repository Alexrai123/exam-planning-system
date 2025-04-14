from pydantic import BaseModel
from typing import Optional
from .user import UserResponse

class ProfessorBase(BaseModel):
    name: str
    specialization: Optional[str] = None
    title: Optional[str] = None
    user_id: Optional[int] = None

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorUpdate(BaseModel):
    specialization: Optional[str] = None
    title: Optional[str] = None
    user_id: Optional[int] = None

class ProfessorResponse(ProfessorBase):
    user: Optional[UserResponse] = None
    
    class Config:
        orm_mode = True
