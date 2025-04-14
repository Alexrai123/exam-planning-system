from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    name: str
    profesor_name: str
    credits: Optional[int] = None
    year: Optional[int] = None
    semester: Optional[int] = None
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    profesor_name: Optional[str] = None
    credits: Optional[int] = None
    year: Optional[int] = None
    semester: Optional[int] = None
    description: Optional[str] = None

class CourseResponse(CourseBase):
    id: int
    
    class Config:
        orm_mode = True
