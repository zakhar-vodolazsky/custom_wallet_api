import decimal
import uuid
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import (
    UUID,
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.transactions import Transaction
    from src.models.users import User


class WalletStatus(StrEnum):
    ACTIVE = "active"
    DELETED = "deleted"
    BLOCKED = "blocked"


class Wallet(MappedAsDataclass, Base):
    __tablename__ = "wallets"

    __table_args__ = CheckConstraint("balance >= 0", name="ck_wallets_balance_non_negative")

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        init=False,
    )

    currency: Mapped[str] = mapped_column(String, nullable=False)

    balance: Mapped[decimal.Decimal] = mapped_column(
        Numeric(scale=2, asdecimal=True), nullable=False, server_default=text("0"), init=False
    )
    public_wallet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default_factory=uuid.uuid4, unique=True, nullable=False, init=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), init=False
    )

    status: Mapped[WalletStatus] = mapped_column(
        nullable=False, server_default=WalletStatus.ACTIVE, index=True, init=False
    )

    user: Mapped[User] = relationship(back_populates="wallet")
    transactions: Mapped[list[Transaction]] = relationship(back_populates="wallet", init=False)
