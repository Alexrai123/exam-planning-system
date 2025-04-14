from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from ..db.base import Base

class Sala(Base):
    __tablename__ = "sala"

    # Name as primary key
    name = Column(String(50), primary_key=True, index=True)
    building = Column(String(50), nullable=True)
    capacity = Column(Integer, nullable=True)
    computers = Column(Integer, nullable=True)
    
    # Relationships
    exams = relationship("Exam", back_populates="sala")
    
    def __repr__(self):
        return f"<Sala {self.name}>"
