import uuid

import pytest
from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.anyio
async def test_wallet_not_found():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get(f"/api/v1/wallets/{uuid.uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet not found"}


@pytest.mark.anyio
async def test_invalid_wallet_uuid():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/api/v1/wallets/not-a-uuid")

    assert response.status_code == 422


@pytest.mark.anyio
async def test_wallet_operation_not_found():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            f"/api/v1/wallets/{uuid.uuid4()}/operation",
            json={
                "operation_type": "DEPOSIT",
                "amount": 1000,
            },
        )

    assert response.status_code == 404
    assert response.json() == {"detail": "Wallet not found"}


@pytest.mark.anyio
async def test_invalid_wallet_operation_uuid():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            "/api/v1/wallets/not-a-uuid/operation",
            json={
                "operation_type": "DEPOSIT",
                "amount": 1000,
            },
        )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_wallet_operation_with_invalid_amount():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            f"/api/v1/wallets/{uuid.uuid4()}/operation",
            json={
                "operation_type": "DEPOSIT",
                "amount": "text",
            },
        )

    assert response.status_code == 422


@pytest.mark.anyio
async def test_wallet_operation_with_invalid_operation_type():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            f"/api/v1/wallets/{uuid.uuid4()}/operation",
            json={
                "operation_type": "INVALID_OPERATION",
                "amount": 1000,
            },
        )

    assert response.status_code == 422
