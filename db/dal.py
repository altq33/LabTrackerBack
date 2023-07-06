from uuid import UUID

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from utils.hasher import Hasher

"""Слой доступа к БД"""


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, username: str, email: str, password: str) -> User:
        new_user = User(
            username=username,
            email=email,
            hashed_password=Hasher.get_hashed_password(password)
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        await self.db_session.commit()
        return new_user

    async def delete_user(self, user_id: UUID) -> UUID | None:
        query = delete(User).where(User.id == user_id).returning(User.id)
        res = await self.db_session.execute(query)
        await self.db_session.commit()
        deleted_user_row = res.fetchone()
        if deleted_user_row:
            return deleted_user_row[0]

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row:
            return user_row[0]

    async def update_user(self, user_id: UUID,  **kwargs) -> UUID | None:
        query = update(User).where(User.id == user_id).values(kwargs).returning(User.id)
        res = await self.db_session.execute(query)
        await self.db_session.commit()
        updated_user_row = res.fetchone()
        if updated_user_row:
            return updated_user_row[0]
