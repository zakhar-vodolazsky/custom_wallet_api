from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings

engine = create_async_engine(
    url=settings().database_url,
    echo=True,
    pool_pre_ping=True,
    hide_parameters=True,
    pool_size=10,
    max_overflow=10,
)

SessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionFactory() as session:
        yield session
