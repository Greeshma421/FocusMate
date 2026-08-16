from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.sessions_service import SessionsService
from app.schemas.study_session import StudySessionCreate, StudySessionRead, StudySessionUpdate
from app.models.user import User

router = APIRouter()


@router.post("/sessions", response_model=StudySessionRead, status_code=status.HTTP_201_CREATED)
async def create_session(session_in: StudySessionCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SessionsService(db, current_user.id)
    session = await service.create_session(session_in)
    return session


@router.get("/sessions", response_model=List[StudySessionRead])
async def list_sessions(start: Optional[datetime] = None, end: Optional[datetime] = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SessionsService(db, current_user.id)
    sessions = await service.list_sessions(start=start, end=end)
    return sessions


@router.get("/sessions/{session_id}", response_model=StudySessionRead)
async def get_session(session_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SessionsService(db, current_user.id)
    session = await service.get_session(session_id)
    return session


@router.put("/sessions/{session_id}", response_model=StudySessionRead)
async def update_session(session_id: UUID, updates: StudySessionUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SessionsService(db, current_user.id)
    session = await service.update_session(session_id, updates)
    return session


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SessionsService(db, current_user.id)
    await service.delete_session(session_id)
    return None


@router.post("/sessions/{session_id}/complete", response_model=StudySessionRead)
async def mark_complete(session_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = SessionsService(db, current_user.id)
    session = await service.mark_complete(session_id)
    return session
