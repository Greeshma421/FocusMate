from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from typing import Optional


engine = None
AsyncSessionLocal: Optional[sessionmaker] = None


def _init_engine():
    global engine, AsyncSessionLocal
    if engine is None or AsyncSessionLocal is None:
        engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
        AsyncSessionLocal = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )


# Dependency for FastAPI routes
async def get_db() -> AsyncSession:
    # Lazy initialize engine/sessionmaker so import-time doesn't require DB drivers
    if AsyncSessionLocal is None:
        _init_engine()
    assert AsyncSessionLocal is not None
    async with AsyncSessionLocal() as session:
        yield session
