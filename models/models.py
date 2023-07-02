import uuid
from datetime import datetime
from sqlalchemy import MetaData, String, TIMESTAMP, Column, UUID
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, sessionmaker

from config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/\
{settings.db_name}"
Base: DeclarativeMeta = declarative_base()

engine: AsyncEngine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

metadata = MetaData()


async def get_session() -> AsyncSession:
	async with async_session() as session:
		yield session


class User(Base):
	__tablename__ = 'users'

	id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
	metadata = metadata
	email = Column(
		String(length=320), unique=True, index=True, nullable=False
	)
	hashed_password = Column(
		String(length=1024), nullable=False
	)
	username = Column(String, unique=True, nullable=False)
	created = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
