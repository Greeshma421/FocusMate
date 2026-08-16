from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notification import Notification
from datetime import datetime
from typing import List
from uuid import UUID


class NotificationRepository:
    @staticmethod
    async def create_notification(db: AsyncSession, user_id: UUID, session_id: UUID, notification_type: str, scheduled_at: datetime, provider_reference: str = None) -> Notification:
        notif = Notification(
            user_id=user_id,
            session_id=session_id,
            notification_type=notification_type,
            scheduled_at=scheduled_at,
        )
        async with db.begin():
            db.add(notif)  # type: ignore[attr-defined]
            await db.flush()
        await db.refresh(notif)
        return notif

    @staticmethod
    async def create_notifications_bulk(db: AsyncSession, user_id: UUID, session_id: UUID, notification_type: str, scheduled_ats: List[datetime]):
        notifs = []
        async with db.begin():
            for sched in scheduled_ats:
                n = Notification(
                    user_id=user_id,
                    session_id=session_id,
                    notification_type=notification_type,
                    scheduled_at=sched,
                )
                db.add(n)  # type: ignore[attr-defined]
                notifs.append(n)
            await db.flush()
        for n in notifs:
            await db.refresh(n)
        return notifs
