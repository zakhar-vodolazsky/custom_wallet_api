import uuid
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import UUID, BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.wallets import Wallet


class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETED"
    BLOCKED = "BLOCKED"


class User(MappedAsDataclass, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True, init=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    password_hash: Mapped[str] = mapped_column(String, nullable=False, repr=False)

    public_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True, default_factory=uuid.uuid4, init=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        init=False,
        server_default=func.now(),
    )
    status: Mapped[UserStatus] = mapped_column(
        nullable=False, server_default=UserStatus.ACTIVE, init=False, index=True
    )
    wallet: Mapped[Wallet] = relationship(back_populates="user", init=False)

    def __post_init__(self) -> None:
        self.username = f"user_{self.public_user_id.hex[:12]}"
