from sqlalchemy import Column, String, Integer
from ..db.base import Base

class Faculty(Base):
    __tablename__ = "faculties"
    
    id = Column(String(10), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    short_name = Column(String(20), nullable=True)
