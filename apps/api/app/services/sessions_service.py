from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.session_repo import SessionRepository
from app.schemas.study_session import StudySessionCreate, StudySessionUpdate
from app.models.study_session import StudySession
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, status
from typing import List, Optional


class SessionsService:
    def __init__(self, db: AsyncSession, user_id: UUID):
        self.db = db
        self.user_id = user_id

    async def create_session(self, session_in: StudySessionCreate) -> StudySession:
        # Basic validations
        if session_in.user_id != self.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create session for another user")

        if session_in.end_at <= session_in.start_at:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="end_at must be after start_at")

        # Check overlaps
        overlaps = await SessionRepository.find_overlapping(self.db, self.user_id, session_in.start_at, session_in.end_at)
        if overlaps:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Session overlaps with existing session")

        # Persist
        session = await SessionRepository.create_session(self.db, session_in)

        # Schedule notifications (default offsets)
        try:
            from app.repositories.notification_repo import NotificationRepository
            from app.core.config import settings
            from datetime import timedelta

            offsets = getattr(settings, "REMINDER_OFFSETS_MINUTES", [10])
            scheduled_ats = [session.start_at - timedelta(minutes=int(m)) for m in offsets]
            # create reminder notifications
            await NotificationRepository.create_notifications_bulk(self.db, self.user_id, session.id, "reminder", scheduled_ats)
        except Exception:
            # Do not fail session creation due to notification scheduling issues; log in future
            pass

        return session

    async def update_session(self, session_id: UUID, updates: StudySessionUpdate) -> StudySession:
        obj = await SessionRepository.get_by_id(self.db, session_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        if obj.user_id != self.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

        new_start = updates.start_at if updates.start_at is not None else obj.start_at
        new_end = updates.end_at if updates.end_at is not None else obj.end_at
        if new_end <= new_start:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="end_at must be after start_at")

        overlaps = await SessionRepository.find_overlapping(self.db, self.user_id, new_start, new_end, exclude_session_id=session_id)
        if overlaps:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Updated session overlaps with existing session")

        # Apply updates
        updates_dict = updates.dict(exclude_unset=True)
        updated = await SessionRepository.update_session(self.db, obj, **updates_dict)
        return updated

    async def delete_session(self, session_id: UUID) -> None:
        obj = await SessionRepository.get_by_id(self.db, session_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        if obj.user_id != self.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        await SessionRepository.delete_session(self.db, obj)

    async def get_session(self, session_id: UUID) -> StudySession:
        obj = await SessionRepository.get_by_id(self.db, session_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        if obj.user_id != self.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        return obj

    async def list_sessions(self, start: Optional[datetime] = None, end: Optional[datetime] = None) -> List[StudySession]:
        return await SessionRepository.list_sessions(self.db, self.user_id, start=start, end=end)

    async def mark_complete(self, session_id: UUID) -> StudySession:
        obj = await self.get_session(session_id)
        updated = await SessionRepository.update_session(self.db, obj, status='completed')
        return updated
