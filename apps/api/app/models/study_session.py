import uuid
from sqlalchemy import Column, String, Enum, Text, Integer, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.base import Base
import enum


class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class StudyType(str, enum.Enum):
    learning = "learning"
    practice = "practice"
    revision = "revision"
    assessment = "assessment"


class SessionStatus(str, enum.Enum):
    planned = "planned"
    completed = "completed"
    paused = "paused"
    missed = "missed"


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    subtopic = Column(String(255), nullable=True)
    start_at = Column(TIMESTAMP(timezone=True), nullable=False)
    end_at = Column(TIMESTAMP(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    priority = Column(Enum(Priority), server_default=Priority.medium.value, nullable=False)
    study_type = Column(Enum(StudyType), server_default=StudyType.learning.value, nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(Enum(SessionStatus), server_default=SessionStatus.planned.value, nullable=False)
    ai_generated = Column(Boolean, server_default="false", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("end_at > start_at", name="ck_session_end_after_start"),
    )
