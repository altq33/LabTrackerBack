from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.dal import UserDAL
from models.models import CreateUser, ShowUser, ShowDeletedUser

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
