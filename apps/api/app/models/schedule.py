import uuid
from sqlalchemy import Column, String, Enum, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.base import Base
import enum


class ScheduleStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    completed = "completed"


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from sqlalchemy import ForeignKey
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("study_goals.id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum(ScheduleStatus), server_default=ScheduleStatus.active.value, nullable=False)
    ai_generated = Column(Boolean, server_default="false", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
