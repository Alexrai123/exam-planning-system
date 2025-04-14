from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..db.base import Base

class Sala(Base):
    __tablename__ = "sala"

    # Name as primary key
    name = Column(String(50), primary_key=True, index=True)
    
    # Relationships
    exams = relationship("Exam", back_populates="sala")
    
    def __repr__(self):
        return f"<Sala {self.name}>"
