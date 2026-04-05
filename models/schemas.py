from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#Base student schema with common fields.
class StudentBase(BaseModel):
    name: str
    age: int
    reg_no: str
    department: str

class StudentCreate(StudentBase):
    """
    Schema for creating new students.
    Inherits all fields from StudentBase.
    """
    pass

class StudentUpdate(BaseModel):
    """
    Schema for updating existing students.
    All fields are optional for partial updates.
    """
    name: Optional[str] = None
    age: Optional[int] = None
    reg_no: Optional[str] = None
    department: Optional[str] = None

class StudentResponse(StudentBase):
    """
    Schema for student response data.
    Includes database-generated fields.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        """Pydantic configuration for ORM compatibility."""
        from_attributes = True
