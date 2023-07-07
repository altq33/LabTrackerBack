from uuid import UUID

from sqlalchemy import insert, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import CreateUser, ShowUser, ShowDeletedUser, ShowUpdatedUser, UpdateUserRequest
from src.auth.models import User
from src.auth.utils import Hasher

"""Services"""


async def create_new_user(user: CreateUser, db_session: AsyncSession) -> ShowUser:
    query = insert(User).values(hashed_password=Hasher.get_hashed_password(user.password), email=user.email,
                                username=user.username).returning(User)
    res = await db_session.execute(query)
    new_user = res.fetchone()[0]
    await db_session.commit()
    return ShowUser(
        username=new_user.username,
        email=new_user.email,
        created=new_user.created,
    )


async def delete_user_by_id(user_id: UUID, db_session: AsyncSession) -> ShowDeletedUser | None:
    query = delete(User).where(User.id == user_id).returning(User.id)
    res = await db_session.execute(query)
    await db_session.commit()
    deleted_user_row = res.fetchone()
    if deleted_user_row is not None:
        return ShowDeletedUser(id=deleted_user_row[0])


async def get_user_by_id(user_id: UUID, db_session: AsyncSession) -> ShowUser | None:
    query = select(User).where(User.id == user_id)
    res = await db_session.execute(query)
    user_row = res.fetchone()
    if user_row:
        return ShowUser(username=user_row[0].username,
                        email=user_row[0].email,
                        created=user_row[0].created
                        )


async def update_user(user_id: UUID, body: UpdateUserRequest, db_session: AsyncSession) -> ShowUpdatedUser | None:
    query = update(User).where(User.id == user_id).values(**body.dict(exclude_none=True)).returning(User.id)
    res = await db_session.execute(query)
    await db_session.commit()
    updated_user_row = res.fetchone()
    return ShowUpdatedUser(id=updated_user_row[0])
