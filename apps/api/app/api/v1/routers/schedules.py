from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.schedules_service import SchedulesService
from app.schemas.schedule import ScheduleCreate, ScheduleRead, ScheduleUpdate
from app.models.user import User

router = APIRouter()


@router.post("/schedules", response_model=ScheduleRead, status_code=status.HTTP_201_CREATED)
async def create_schedule(schedule_in: ScheduleCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SchedulesService(db, current_user.id)
    sched = await service.create_schedule(schedule_in)
    return sched


@router.get("/schedules", response_model=List[ScheduleRead])
async def list_schedules(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SchedulesService(db, current_user.id)
    items = await service.list_schedules()
    return items


@router.get("/schedules/{schedule_id}", response_model=ScheduleRead)
async def get_schedule(schedule_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SchedulesService(db, current_user.id)
    return await service.get_schedule(schedule_id)


@router.put("/schedules/{schedule_id}", response_model=ScheduleRead)
async def update_schedule(schedule_id: UUID, updates: ScheduleUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SchedulesService(db, current_user.id)
    return await service.update_schedule(schedule_id, updates)


@router.delete("/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(schedule_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SchedulesService(db, current_user.id)
    await service.delete_schedule(schedule_id)
    return None
