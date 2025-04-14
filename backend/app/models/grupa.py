from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base import Base

class Grupa(Base):
    __tablename__ = "grupa"

    # Name as primary key
    name = Column(String(50), primary_key=True, index=True)
    year = Column(Integer, nullable=True)
    specialization = Column(String(100), nullable=True)
    leader_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    exams = relationship("Exam", back_populates="grupa")
    leader = relationship("User", back_populates="led_groups")
    
    def __repr__(self):
        return f"<Grupa {self.name}>"
