from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.schedule import ScheduleStatus


class ScheduleBase(BaseModel):
    title: str
    goal_id: Optional[UUID] = None
    status: ScheduleStatus = ScheduleStatus.active
    ai_generated: bool = False


class ScheduleCreate(ScheduleBase):
    user_id: UUID

    class Config:
        orm_mode = True


class ScheduleUpdate(BaseModel):
    title: Optional[str]
    goal_id: Optional[UUID]
    status: Optional[ScheduleStatus]
    ai_generated: Optional[bool]

    class Config:
        orm_mode = True


class ScheduleRead(ScheduleBase):
    id: UUID
    user_id: UUID
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
