from uuid import UUID

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User

"""Слой доступа к БД"""


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

    async def delete_user(self, user_id: UUID) -> UUID | None:
        query = delete(User).where(User.id == user_id).returning(User)
        res = await self.db_session.execute(query)
