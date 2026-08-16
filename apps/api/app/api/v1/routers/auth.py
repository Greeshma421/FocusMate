from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead, Token
from app.models.user import User
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # check existing
    q = select(User).where(User.email == user_in.email)
    res = await db.execute(q)
    existing = res.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User()
    user.email = user_in.email
    user.name = user_in.name
    user.password_hash = AuthService.hash_password(user_in.password)
    async with db.begin():
        db.add(user)  # type: ignore[attr-defined]
        await db.flush()
    await db.refresh(user)
    return user


@router.post("/auth/login", response_model=Token)
async def login(form_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # for simplicity accept email+password in same schema
    q = select(User).where(User.email == form_data.email)
    res = await db.execute(q)
    user = res.scalars().first()
    if not user or not AuthService.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = AuthService.create_access_token({"sub": str(user.id)})
    return Token(access_token=token)
