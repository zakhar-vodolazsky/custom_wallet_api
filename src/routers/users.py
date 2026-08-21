import asyncio

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.models.users import User
from src.schemas.users import UserCreate, UserRead
from src.security.password import hash_password
from src.validators.session_dep import SessionDep

router = APIRouter(tags=["Users"])


@router.post("/users", response_model=UserRead)
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
