import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_schedules_routes_exist():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get('/api/v1/schedules')
        assert r.status_code in (200, 401)
