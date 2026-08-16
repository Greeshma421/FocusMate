from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories.schedule_repo import ScheduleRepository
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate
from app.models.schedule import Schedule


class SchedulesService:
    def __init__(self, db: AsyncSession, user_id: UUID):
        self.db = db
        self.user_id = user_id

    async def create_schedule(self, schedule_in: ScheduleCreate) -> Schedule:
        if schedule_in.user_id != self.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create schedule for another user")
        sched = await ScheduleRepository.create_schedule(self.db, schedule_in)
        return sched

    async def get_schedule(self, schedule_id: UUID) -> Schedule:
        obj = await ScheduleRepository.get_by_id(self.db, schedule_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        if obj.user_id != self.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        return obj

    async def list_schedules(self) -> List[Schedule]:
        return await ScheduleRepository.list_schedules(self.db, user_id=self.user_id)

    async def update_schedule(self, schedule_id: UUID, updates: ScheduleUpdate) -> Schedule:
        obj = await ScheduleRepository.get_by_id(self.db, schedule_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        if obj.user_id != self.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        updates_dict = updates.dict(exclude_unset=True)
        updated = await ScheduleRepository.update_schedule(self.db, obj, **updates_dict)
        return updated

    async def delete_schedule(self, schedule_id: UUID) -> None:
        obj = await ScheduleRepository.get_by_id(self.db, schedule_id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        if obj.user_id != self.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        await ScheduleRepository.delete_schedule(self.db, obj)
