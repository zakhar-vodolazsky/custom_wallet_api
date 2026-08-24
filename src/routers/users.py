import asyncio

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from schemas.session_dep import SessionDep
from src.models.users import User
from src.schemas.auth import BasicAuth
from src.schemas.users import UserCreate, UserRead
from src.security.password import DUMMY_PASSWORD_HASH, hash_password, verify_password

router = APIRouter(tags=["Users"])


@router.post("/users", response_model=UserRead, status_code=201)
async def create_user(payload: UserCreate, session: SessionDep) -> User:
    hashed_password = await asyncio.to_thread(hash_password, payload.password)
    user = User(email=payload.email, password_hash=hashed_password)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account wth this email already exists. Sign in or reset your password.",
        ) from exc

    return user


@router.post("/login", tags=["Auth"], response_model=UserRead)
async def verify_user(payload: BasicAuth, session: SessionDep) -> User:
    try:
        user: User | None = await session.scalar(select(User).where(User.email == payload.email))
    except RuntimeError, SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Internal server error") from None
    if not user:
        verify_password(payload.password, DUMMY_PASSWORD_HASH)
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return user
