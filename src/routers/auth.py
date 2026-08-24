from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
import logging
from src.models.users import User
from src.schemas.auth import BasicAuth
from src.schemas.users import UserRead
from src.security.password import DUMMY_PASSWORD_HASH, verify_password
from src.validators.session_dep import SessionDep

router = APIRouter()

logger = logging.getLogger(__name__)
@router.post("/login", tags=["Auth"], response_model=UserRead)
async def login(payload: BasicAuth, session: SessionDep) -> User:
    try:
        user: User | None = await session.scalar(select(User).where(User.email == payload.email))
    except RuntimeError, SQLAlchemyError:
        logger.error(msg="Database error during login")
        raise HTTPException(status_code=500, detail="Internal server error") from None
    if not user:
        verify_password(payload.password, DUMMY_PASSWORD_HASH)
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return user
