from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    completed: Optional[bool] = None