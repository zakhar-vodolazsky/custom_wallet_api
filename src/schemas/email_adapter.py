from typing import Annotated

from pydantic import AfterValidator, EmailStr


def normalize_email(value: str) -> str:
    return value.lower()


Email = Annotated[EmailStr, AfterValidator(normalize_email)]
