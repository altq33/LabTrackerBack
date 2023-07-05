from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.dal import UserDAL
from models.models import CreateUser, ShowUser, ShowDeletedUser, ShowUpdatedUser, UpdateUserRequest

"""Сервисы"""


async def create_new_user(user: CreateUser, db_session: AsyncSession) -> ShowUser:
    user_dal = UserDAL(db_session)
    new_user = await user_dal.create_user(
        username=user.username,
        email=user.email,
        password=user.password
    )
    return ShowUser(
        username=new_user.username,
        email=new_user.email,
        created=new_user.created
    )


async def delete_user(user_id: UUID, db_session: AsyncSession) -> ShowDeletedUser | None:
    user_dal = UserDAL(db_session)
    deleted_user_id = await user_dal.delete_user(user_id)
    if deleted_user_id:
        return ShowDeletedUser(id=deleted_user_id)


async def get_user_by_id(user_id: UUID, db_session: AsyncSession) -> ShowUser | None:
    user_dal = UserDAL(db_session)
    user = await user_dal.get_user_by_id(user_id)
    if user:
        return ShowUser(username=user.username,
                        email=user.email,
                        created=user.created
                        )


async def update_user(user_id: UUID, body: UpdateUserRequest, db_session: AsyncSession) -> ShowUpdatedUser | None:
    user_dal = UserDAL(db_session)
    updated_user_id = await user_dal.update_user(user_id, **body.dict(exclude_none=True))
    return ShowUpdatedUser(id=updated_user_id)
