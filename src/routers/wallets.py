from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.models import Wallet
from src.schemas import WalletBalance
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
