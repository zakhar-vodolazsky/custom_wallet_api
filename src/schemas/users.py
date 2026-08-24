from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from src.validators import Email, Password


class UserCreate(BaseModel):
    email: Email
    password: Password


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    public_user_id: UUID
    wallet_uuid: UUID
    email: str
    created_at: datetime
