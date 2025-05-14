from typing import Optional
from pydantic import BaseModel

# Base model for shared attributes
class SpecializationBase(BaseModel):
    name: str
    code: str
    faculty_id: int

# Model for creating a new specialization
class SpecializationCreate(SpecializationBase):
    pass

# Model for updating an existing specialization
class SpecializationUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    faculty_id: Optional[int] = None

# Model for response with all attributes
class SpecializationResponse(SpecializationBase):
    id: int

    class Config:
        from_attributes = True  # This replaces orm_mode=True in Pydantic v2
