import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.db.base import Base
import enum


class QuestionType(str, enum.Enum):
    mcq = "mcq"
    truefalse = "truefalse"
    short = "short"
    coding = "coding"


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(Enum(QuestionType), nullable=False)
    prompt = Column(Text, nullable=False)
    choices = Column(JSONB, nullable=True)
    correct_answer = Column(JSONB, nullable=True)
    # 'metadata' is reserved on declarative Base; use 'meta' attribute mapped to DB column 'metadata'
    meta = Column('metadata', JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
