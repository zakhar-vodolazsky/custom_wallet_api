from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from typing import Annotated, LiteralString

from pydantic import AfterValidator, Field
from pydantic_core import PydanticCustomError

ALLOWED_CHARACTERS = ascii_lowercase + ascii_uppercase + digits + punctuation


INVALID_CHARACTER_MESSAGE: LiteralString = (
    "Password should contain only Latin letters, digits and special characters: {special_chars}"
)


def validate_password(p: str) -> str:
    if any(char not in ALLOWED_CHARACTERS for char in p):
        raise PydanticCustomError(
            "invalid_character", INVALID_CHARACTER_MESSAGE, {"special_chars": punctuation}
        )

    if not any(char in ascii_uppercase for char in p):
        raise PydanticCustomError("no_uppercase_character", "Missing uppercase character")

    if not any(char in ascii_lowercase for char in p):
        raise PydanticCustomError("no_lowercase_character", "Missing lowercase character")

    if not any(char in digits for char in p):
        raise PydanticCustomError("no_digit", "Missing digit")

    if not any(char in punctuation for char in p):
        raise PydanticCustomError("no_special_character", "Missing special character")

    return p


Password = Annotated[str, Field(min_length=8, max_length=128), AfterValidator(validate_password)]
