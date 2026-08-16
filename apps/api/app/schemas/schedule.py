from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from app.models.schedule import ScheduleStatus


class ScheduleCreate(BaseModel):
    user_id: UUID
    title: str
    goal_id: Optional[UUID] = None
    status: ScheduleStatus = ScheduleStatus.active
    ai_generated: bool = False

    class Config:
        orm_mode = True
