from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from ..db.base import Base
import enum
from datetime import datetime

class ExamStatus(str, enum.Enum):
    PROPOSED = "proposed"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    grupa_name = Column(String(50), ForeignKey("grupa.name"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    sala_name = Column(String(50), ForeignKey("sala.name"), nullable=False)
    status = Column(Enum(ExamStatus), default=ExamStatus.PROPOSED, nullable=False)
    professor_agreement = Column(Boolean, default=False, nullable=False)
    professor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    course = relationship("Course", back_populates="exams")
    grupa = relationship("Grupa", back_populates="exams")
    sala = relationship("Sala", back_populates="exams")
    professor = relationship("User", foreign_keys=[professor_id])
    
    def __repr__(self):
        return f"<Exam {self.course.name} for {self.grupa.name} on {self.date}>"
