from typing import Generator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base

from src.config import settings


"""Creating DB session and function for DI"""

DATABASE_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/\
{settings.db_name}"
Base: DeclarativeMeta = declarative_base()

engine: AsyncEngine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


"""Global session for all operations"""


async def get_session() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
