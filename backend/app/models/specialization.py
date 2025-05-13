from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import Base

class Specialization(Base):
    """
    Specialization model for representing university specializations
    """
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    code = Column(String, index=True, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    
    # Relationships
    faculty = relationship("Faculty", back_populates="specializations")
    groups = relationship("Group", back_populates="specialization")
