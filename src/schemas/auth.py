from pydantic import BaseModel

from schemas.email_adapter import Email


class BasicAuth(BaseModel):
    email: Email
    password: str
