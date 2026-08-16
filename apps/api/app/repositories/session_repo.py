from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from app.models.study_session import StudySession
from app.schemas.study_session import StudySessionCreate
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class SessionRepository:
    @staticmethod
    async def create_session(db: AsyncSession, session_in: StudySessionCreate) -> StudySession:
        session = StudySession(
            id=session_in.id,
            schedule_id=session_in.schedule_id,
            user_id=session_in.user_id,
            name=session_in.name,
            topic_id=session_in.topic_id,
            subtopic=session_in.subtopic,
            start_at=session_in.start_at,
            end_at=session_in.end_at,
            duration_minutes=session_in.duration_minutes,
            priority=session_in.priority,
            study_type=session_in.study_type,
            notes=session_in.notes,
            status=session_in.status,
            ai_generated=session_in.ai_generated,
        )
        async with db.begin():
            db.add(session)  # type: ignore[attr-defined]
            await db.flush()
        await db.refresh(session)
        return session

    @staticmethod
    async def find_overlapping(db: AsyncSession, user_id: UUID, start_at: datetime, end_at: datetime, exclude_session_id: Optional[UUID] = None) -> List[StudySession]:
        # overlap if existing.start < new_end AND existing.end > new_start
        q = select(StudySession).where(
            StudySession.user_id == user_id,
            StudySession.start_at < end_at,
            StudySession.end_at > start_at,
        )
        if exclude_session_id:
            q = q.where(StudySession.id != exclude_session_id)
        res = await db.execute(q)
        return res.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, session_id: UUID) -> Optional[StudySession]:
        q = select(StudySession).where(StudySession.id == session_id)
        res = await db.execute(q)
        return res.scalars().first()

    @staticmethod
    async def update_session(db: AsyncSession, session_obj: StudySession, **updates) -> StudySession:
        for key, value in updates.items():
            if hasattr(session_obj, key) and value is not None:
                setattr(session_obj, key, value)
        async with db.begin():
            db.add(session_obj)  # type: ignore[attr-defined]
            await db.flush()
        await db.refresh(session_obj)
        return session_obj

    @staticmethod
    async def delete_session(db: AsyncSession, session_obj: StudySession) -> None:
        async with db.begin():
            await db.delete(session_obj)

    @staticmethod
    async def list_sessions(db: AsyncSession, user_id: UUID, start: Optional[datetime] = None, end: Optional[datetime] = None) -> List[StudySession]:
        q = select(StudySession).where(StudySession.user_id == user_id)
        if start:
            q = q.where(StudySession.start_at >= start)
        if end:
            q = q.where(StudySession.end_at <= end)
        res = await db.execute(q)
        return res.scalars().all()
