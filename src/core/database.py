from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config import app_config

async_engine = create_async_engine(
    url=app_config.default_asyncpg_url,
    echo=app_config.ECHO,
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False, autocommit=False, autoflush=False)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


SessionAnnotated = Annotated[AsyncSession, Depends(get_async_session)]
