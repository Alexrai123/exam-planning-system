from pydantic import BaseModel
from typing import Optional

class SalaBase(BaseModel):
    name: str

class SalaCreate(SalaBase):
    pass

class SalaUpdate(BaseModel):
    name: Optional[str] = None

class SalaResponse(SalaBase):
    class Config:
        orm_mode = True
