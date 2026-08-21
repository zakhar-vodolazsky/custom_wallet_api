from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from src.validators.password import Password


class UserCreate(BaseModel):
    email: EmailStr
    password: Password


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    public_id: UUID
    email: EmailStr
    created_at: datetime
