import uuid
from sqlalchemy import Column, Float, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from app.db.base import Base


class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False, server_default="0")
    answers = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
