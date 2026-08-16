import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, Integer, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base
import enum


class NotificationType(str, enum.Enum):
    reminder = "reminder"
    revision = "revision"
    assessment = "assessment"


class NotificationStatus(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    failed = "failed"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("study_sessions.id", ondelete="CASCADE"), nullable=True, index=True)
    notification_type = Column(Enum(NotificationType), nullable=False)
    scheduled_at = Column(TIMESTAMP(timezone=True), nullable=False)
    sent_at = Column(TIMESTAMP(timezone=True), nullable=True)
    status = Column(Enum(NotificationStatus), server_default=NotificationStatus.pending.value, nullable=False)
    retries = Column(Integer, server_default="0", nullable=False)
    provider_reference = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
