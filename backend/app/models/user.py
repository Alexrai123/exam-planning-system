from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from ..db.base import Base
import enum

class UserRole(str, enum.Enum):
    STUDENT = "STUDENT"
    PROFESSOR = "PROFESSOR"
    SECRETARIAT = "SECRETARIAT"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    
    # Relationships
    professor = relationship("Professor", back_populates="user", uselist=False)
    led_groups = relationship("Grupa", back_populates="leader")
    
    def __repr__(self):
        return f"<User {self.name}>"
