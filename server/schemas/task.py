from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
import uuid

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    color: str

class Task(TaskBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    createdAt: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Sample Task",
                "description": "This is a sample task",
                "status": "todo",
                "createdAt": "2023-01-01T00:00:00"
            }
        }