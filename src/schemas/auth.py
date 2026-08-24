from pydantic import BaseModel

from src.validators.email import Email


class BasicAuth(BaseModel):
    email: Email
    password: str
