from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import insert, delete, select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.schemas import CreateUser, ShowUser, ShowDeletedUser, ShowUpdatedUser, UpdateUserRequest, UserInDB
from src.auth.utils import Hasher

"""Services"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth")


async def create_new_user(user: CreateUser, db_session: AsyncSession) -> ShowUser | None:
    user_by_email = await get_user_by_username(user.email, db_session)
    user_by_username = await get_user_by_username(user.username, db_session)
    if user_by_email or user_by_username:
        return

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


async def get_user_by_id(user_id: UUID, db_session: AsyncSession) -> UserInDB | None:
    query = select(User).where(User.id == user_id)
    res = await db_session.execute(query)
    user_row = res.fetchone()
    if user_row:
        return UserInDB(id=user_row[0].id,
                        username=user_row[0].username,
                        email=user_row[0].email,
                        created=user_row[0].created,
                        hashed_password=user_row[0].hashed_password,
                        roles=user_row[0].roles
                        )


async def get_user_by_username(username_or_email: str, db_session: AsyncSession) -> UserInDB | None:
    query = select(User).where(or_(User.username == username_or_email, User.email == username_or_email))
    res = await db_session.execute(query)
    selected_user = res.fetchone()
    if selected_user:
        return UserInDB(id=selected_user[0].id,
                        email=selected_user[0].email,
                        hashed_password=selected_user[0].hashed_password,
                        username=selected_user[0].username,
                        created=selected_user[0].created,
                        roles=selected_user[0].roles)


async def update_user(user_id: UUID, body: UpdateUserRequest, db_session: AsyncSession) -> ShowUpdatedUser | None:
    user_by_email = await get_user_by_username(body.email, db_session)
    user_by_username = await get_user_by_username(body.username, db_session)

    if user_by_email and user_by_email.id != user_id:
        return
    if user_by_username and user_by_username.id != user_id:
        return

    query = update(User).where(User.id == user_id).values(**body.dict(exclude_none=True)).returning(User.id)
    res = await db_session.execute(query)
    await db_session.commit()
    updated_user_row = res.fetchone()
    return ShowUpdatedUser(id=updated_user_row[0])


async def authenticate_user(username_or_email: str, password: str, db_session: AsyncSession) -> UserInDB | bool:
    user = await get_user_by_username(username_or_email, db_session)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user
