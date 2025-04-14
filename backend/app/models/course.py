from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..db.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    profesor_name = Column(String(100), ForeignKey("professors.name"), nullable=False)
    credits = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)
    semester = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    professor = relationship("Professor", back_populates="courses")
    exams = relationship("Exam", back_populates="course")
    
    def __repr__(self):
        return f"<Course {self.name}>"
