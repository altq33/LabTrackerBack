from datetime import datetime

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()

metadata = MetaData()


class User(Base):
	__tablename__ = 'user'
	metadata = metadata
	email: Mapped[str] = mapped_column(
		String(length=320), unique=True, index=True, nullable=False
	)
	hashed_password: Mapped[str] = mapped_column(
		String(length=1024), nullable=False
	)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
	is_superuser: Mapped[bool] = mapped_column(
		Boolean, default=False, nullable=False
	)
	is_verified: Mapped[bool] = mapped_column(
		Boolean, default=False, nullable=False
	)
	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, nullable=False)
	created = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
