import asyncio

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.models import User, Wallet
from src.schemas import UserCreate, UserRead
from src.security import hash_password
from src.validators import SessionDep

router = APIRouter(tags=["Users"])


@router.post("/users", response_model=UserRead, status_code=201)
async def create_user(payload: UserCreate, session: SessionDep) -> User:
    hashed_password = await asyncio.to_thread(hash_password, payload.password)
    user = User(email=payload.email, password_hash=hashed_password)
    wallet = Wallet(currency="USD", user=user)
    try:
        async with session.begin():
            session.add_all([user, wallet])
    except IntegrityError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account wth this email already exists. Sign in or reset your password.",
        ) from exc
    return user
