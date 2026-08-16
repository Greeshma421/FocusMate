import uuid
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False)
    revoked = Column(Boolean, server_default="false", nullable=False)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
