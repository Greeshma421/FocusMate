from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate


class ScheduleRepository:
    @staticmethod
    async def create_schedule(db: AsyncSession, schedule_in: ScheduleCreate) -> Schedule:
        sched = Schedule(
            user_id=schedule_in.user_id,
            title=schedule_in.title,
            goal_id=schedule_in.goal_id,
            status=schedule_in.status,
            ai_generated=schedule_in.ai_generated,
        )
        async with db.begin():
            db.add(sched)  # type: ignore[attr-defined]
            await db.flush()
        await db.refresh(sched)
        return sched

    @staticmethod
    async def get_by_id(db: AsyncSession, schedule_id):
        q = select(Schedule).where(Schedule.id == schedule_id)
        res = await db.execute(q)
        return res.scalars().first()

    @staticmethod
    async def update_schedule(db: AsyncSession, schedule_obj: Schedule, **updates) -> Schedule:
        for key, value in updates.items():
            if hasattr(schedule_obj, key) and value is not None:
                setattr(schedule_obj, key, value)
        async with db.begin():
            db.add(schedule_obj)  # type: ignore[attr-defined]
            await db.flush()
        await db.refresh(schedule_obj)
        return schedule_obj

    @staticmethod
    async def delete_schedule(db: AsyncSession, schedule_obj: Schedule) -> None:
        async with db.begin():
            await db.delete(schedule_obj)

    @staticmethod
    async def list_schedules(db: AsyncSession, user_id=None):
        q = select(Schedule)
        if user_id:
            q = q.where(Schedule.user_id == user_id)
        res = await db.execute(q)
        return res.scalars().all()
