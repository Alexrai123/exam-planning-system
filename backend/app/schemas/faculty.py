from pydantic import BaseModel
from typing import Optional

class FacultyBase(BaseModel):
    id: str
    name: str
    short_name: Optional[str] = None

class FacultyCreate(FacultyBase):
    pass

class FacultyUpdate(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None

class FacultyResponse(FacultyBase):
    class Config:
        orm_mode = True
