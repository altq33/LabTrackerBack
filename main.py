from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import DeclarativeMeta, declarative_base
from config import settings
from models.models import User, async_session, get_session

app = FastAPI(title="LabTracker")


class UserDAL:
	def __init__(self, db_session: AsyncSession):
		self.db_session = db_session

	async def create_user(self, username: str, email: str, password: str) -> User:
		new_user = User(
			username=username,
			email=email,
			hashed_password=password
		)
		self.db_session.add(new_user)
		await self.db_session.flush()
		await self.db_session.commit()
		return new_user


@app.get("/")
async def root():
	return {'status': 200, 'message': "Server is OK", 'settings': settings}


class CreateUser(BaseModel):
	username: str
	email: EmailStr
	password: str


@app.post("/reg")
async def registration(user: CreateUser, session: AsyncSession = Depends(get_session)):
	user_dal = UserDAL(session)
	new_user = await user_dal.create_user(
		username=user.username,
		email=user.email,
		password=user.password
	)
	return {'user': new_user}
