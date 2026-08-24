from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.database import engine
from src.core.logger import configure_logging
from src.routers.users import router as users_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    try:
        yield
    finally:
        await engine.dispose()


configure_logging()
app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
