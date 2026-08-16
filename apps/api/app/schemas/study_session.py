from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.study_session import Priority, StudyType, SessionStatus


class StudySessionBase(BaseModel):
    schedule_id: Optional[UUID]
    topic_id: Optional[UUID]
    subtopic: Optional[str]
    name: str
    start_at: datetime
    end_at: datetime
    duration_minutes: int
    priority: Priority = Priority.medium
    study_type: StudyType = StudyType.learning
    notes: Optional[str] = None

    @validator("end_at")
    def end_must_be_after_start(cls, v, values):
        start = values.get("start_at")
        if start and v <= start:
            raise ValueError("end_at must be after start_at")
        return v


class StudySessionCreate(StudySessionBase):
    id: Optional[UUID]
    user_id: UUID
    status: SessionStatus = SessionStatus.planned
    ai_generated: bool = False

    class Config:
        orm_mode = True


class StudySessionUpdate(BaseModel):
    schedule_id: Optional[UUID]
    name: Optional[str]
    topic_id: Optional[UUID]
    subtopic: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    duration_minutes: Optional[int]
    priority: Optional[Priority]
    study_type: Optional[StudyType]
    notes: Optional[str]
    status: Optional[SessionStatus]

    class Config:
        orm_mode = True


class StudySessionRead(StudySessionBase):
    id: UUID
    user_id: UUID
    status: SessionStatus
    ai_generated: bool

    class Config:
        orm_mode = True
