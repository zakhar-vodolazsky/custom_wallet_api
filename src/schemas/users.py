from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from schemas.email_adapter import Email
from schemas.password_adapter import Password


class UserCreate(BaseModel):
    email: Email
    password: Password


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    public_user_id: UUID
    email: str
    created_at: datetime
