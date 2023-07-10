from typing import Annotated
from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import insert, delete, select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException, Depends
from src.auth.schemas import CreateUser, ShowUser, ShowDeletedUser, ShowUpdatedUser, UpdateUserRequest, UserInDB, \
    TokenData, Roles
from src.auth.models import User
from src.auth.utils import Hasher
from src.config import settings
from src.database import get_session

"""Services"""


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/auth")


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


async def get_user_by_username(username_or_email: str, db_session: AsyncSession) -> UserInDB | None:
    query = select(User).where(or_(User.username == username_or_email, User.email == username_or_email))
    res = await db_session.execute(query)
    selected_user = res.fetchone()[0]
    if selected_user:
        return UserInDB(id=selected_user.id, email=selected_user.email, hashed_password=selected_user.hashed_password,
                        username=selected_user.username, created=selected_user.created, roles=selected_user.roles)


async def update_user(user_id: UUID, body: UpdateUserRequest, db_session: AsyncSession) -> ShowUpdatedUser | None:
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


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db_session: Annotated[AsyncSession, Depends(get_session)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        roles: list[Roles] = payload.get("roles")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, roles=roles)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(token_data.username, db_session)
    if user is None:
        raise credentials_exception
    return user
