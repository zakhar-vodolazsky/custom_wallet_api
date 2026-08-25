from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException
from fastapi.openapi.models import Example
from sqlalchemy import select

from src.models import Transaction, TransactionType, Wallet
from src.schemas import WalletBalance, WalletOperation
from src.validators import SessionDep

router = APIRouter(prefix="/api/v1/wallets", tags=["Wallets"])


@router.get("/{wallet_uuid}", response_model=WalletBalance)
async def get_wallet(wallet_uuid: UUID, session: SessionDep) -> WalletBalance:
    wallet: Wallet | None = await session.scalar(
        select(Wallet).where(Wallet.wallet_uuid == wallet_uuid)
    )

    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletBalance(wallet_uuid=wallet.wallet_uuid, balance=wallet.balance)


@router.post(
    "/{wallet_uuid}/operation",
    response_model=WalletBalance,
)
async def change_wallet_balance(
    wallet_uuid: UUID,
    payload: Annotated[
        WalletOperation,
        Body(
            openapi_examples={
                "deposit": Example(
                    summary="Пополнение",
                    value={
                        "operation_type": "DEPOSIT",
                        "amount": 1000,
                    },
                ),
                "withdraw": Example(
                    summary="Списание",
                    value={
                        "operation_type": "WITHDRAW",
                        "amount": 1000,
                    },
                ),
            }
        ),
    ],
    session: SessionDep,
) -> WalletBalance:
    async with session.begin():
        wallet: Wallet | None = await session.scalar(
            select(Wallet).where(Wallet.wallet_uuid == wallet_uuid).with_for_update()
        )

        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail="Wallet not found",
            )

        if payload.operation_type == TransactionType.WITHDRAW:
            if wallet.balance < payload.amount:
                raise HTTPException(
                    status_code=400,
                    detail="Insufficient funds",
                )

            wallet.balance -= payload.amount
        else:
            wallet.balance += payload.amount

        transaction = Transaction(
            operation_type=payload.operation_type,
            amount=payload.amount,
            wallet=wallet,
        )
        session.add(transaction)

    return WalletBalance(
        wallet_uuid=wallet.wallet_uuid,
        balance=wallet.balance,
    )
