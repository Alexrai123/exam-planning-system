from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base import Base

class Professor(Base):
    __tablename__ = "professors"

    # Name as primary key
    name = Column(String(100), primary_key=True, index=True)
    specialization = Column(String(100), nullable=True)
    title = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    courses = relationship("Course", back_populates="professor")
    user = relationship("User", back_populates="professor")
    
    def __repr__(self):
        return f"<Professor {self.name}>"
