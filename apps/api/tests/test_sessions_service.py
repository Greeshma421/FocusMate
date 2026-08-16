import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from app.services.sessions_service import SessionsService
from app.schemas.study_session import StudySessionCreate


class DummyDB:
    pass


@pytest.mark.asyncio
async def test_end_after_start_validation():
    dummy_db = DummyDB()
    user_id = uuid4()
    service = SessionsService(dummy_db, user_id)

    start = datetime.utcnow()
    end = start

    session_in = StudySessionCreate(
        id=uuid4(),
        user_id=user_id,
        name="Test",
        start_at=start,
        end_at=end,
        duration_minutes=60,
    )

    with pytest.raises(Exception):
        await service.create_session(session_in)

# More service tests require DB mock or test DB; keep scaffolding for now.
