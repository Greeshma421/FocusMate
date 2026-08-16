import uuid
from sqlalchemy import Column, String, Date, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.base import Base

import enum


class GoalStatus(str, enum.Enum):
    active = "active"
    paused = "paused"
    completed = "completed"


class StudyGoal(Base):
    __tablename__ = "study_goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from sqlalchemy import ForeignKey
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    target_date = Column(Date, nullable=True)
    status = Column(Enum(GoalStatus), server_default=GoalStatus.active.value, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
