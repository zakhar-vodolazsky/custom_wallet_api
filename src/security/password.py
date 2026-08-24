from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from argon2.profiles import RFC_9106_LOW_MEMORY

hasher = PasswordHasher.from_parameters(RFC_9106_LOW_MEMORY)


DUMMY_PASSWORD_HASH = hasher.hash("dummy-password-used-only-for-verification")


def hash_password(password: str) -> str:
    hashed = hasher.hash(password)
    return hashed


def verify_password(plain: str, hashed: str) -> bool:
    try:
        hasher.verify(hashed, plain)
        return True
    except VerifyMismatchError:
        return False
