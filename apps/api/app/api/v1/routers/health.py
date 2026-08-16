from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter()


@router.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    """Health check endpoint. Verifies DB connectivity."""
    try:
        # simple raw query to check DB
        await db.execute("SELECT 1")
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "ok", "db": f"error: {str(e)}"}
