from pydantic import BaseModel
from typing import Optional


class TaskItem(BaseModel):
    id: int
    title: str
    priority: str  # URGENT, HIGH, FOLLOW-UP
    category: str  # Banking, SIM, Device, Legal, Document
    completed: bool = False
    instructions: Optional[str] = ""


class TaskUpdate(BaseModel):
    task_id: int
    completed: bool
    notes: Optional[str] = ""