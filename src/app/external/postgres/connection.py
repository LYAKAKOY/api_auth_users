from typing import AsyncGenerator
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from loguru import logger

from .models import Base
from ...settings import settings

url = URL.create(
    drivername="postgresql+asyncpg",
    host=settings.postgres.host,
    port=settings.postgres.port,
    username=settings.postgres.user,
    password=settings.postgres.password,
    database=settings.postgres.database,
)
engine = create_async_engine(url)


async def create_tables() -> None:
    async with engine.begin() as connection:
        logger.info('msg="Creating tables..."')
        await connection.run_sync(Base.metadata.create_all)
        logger.info('msg="Tables created"')


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session
