import pytest
from uuid import uuid4
from app.services.schedules_service import SchedulesService
from app.schemas.schedule import ScheduleCreate


class DummyDB:
    pass


@pytest.mark.asyncio
async def test_create_schedule_user_mismatch():
    dummy_db = DummyDB()
    user_id = uuid4()
    service = SchedulesService(dummy_db, user_id)

    payload = ScheduleCreate(user_id=uuid4(), title="Test")
    with pytest.raises(Exception):
        await service.create_schedule(payload)
