from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field

from src.models import TransactionType


class WalletBalance(BaseModel):
    wallet_uuid: UUID
    balance: Decimal


class WalletOperation(BaseModel):
    operation_type: TransactionType
    amount: Annotated[Decimal, Field(gt=0, max_digits=20, decimal_places=2)]
