from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime
from ..models.exam import ExamStatus

class ExamBase(BaseModel):
    course_id: int
    grupa_name: str
    date: date
    time: time
    sala_name: str
    status: ExamStatus = ExamStatus.PROPOSED
    professor_agreement: bool = False
    professor_id: Optional[int] = None

class ExamCreate(ExamBase):
    pass

class ExamUpdate(BaseModel):
    course_id: Optional[int] = None
    grupa_name: Optional[str] = None
    date: Optional[date] = None
    time: Optional[time] = None
    sala_name: Optional[str] = None
    status: Optional[ExamStatus] = None
    professor_agreement: Optional[bool] = None

class ExamStatusUpdate(BaseModel):
    status: ExamStatus

class ProfessorAgreementUpdate(BaseModel):
    professor_agreement: bool

class ExamResponse(BaseModel):
    id: int
    course_id: int
    grupa_name: str
    date: date
    time: time
    sala_name: str
    status: ExamStatus = ExamStatus.PROPOSED
    professor_agreement: bool = False
    professor_name: Optional[str] = None
    professor_id: Optional[int] = None
    
    class Config:
        orm_mode = True
