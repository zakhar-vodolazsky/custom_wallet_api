import decimal
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, CheckConstraint, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.wallets import Wallet


class TransactionType(StrEnum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"


class Transaction(MappedAsDataclass, Base):
    __tablename__ = "transactions"

    __table_args__ = (CheckConstraint("amount <> 0", name="ck_transactions_amount_not_zero"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)

    operation_type: Mapped[TransactionType] = mapped_column(
        nullable=False,
    )

    wallet_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("wallets.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        init=False,
    )

    amount: Mapped[decimal.Decimal] = mapped_column(
        Numeric(scale=2, asdecimal=True),
        nullable=False,
    )
    time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), init=False
    )

    wallet: Mapped[Wallet] = relationship(back_populates="transactions")
