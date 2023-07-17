from typing import Annotated
from uuid import UUID

from fastapi import Depends, Path
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import credentials_exception
from src.auth.schemas import Roles, TokenData, UserInDB
from src.auth.service import get_user_by_username, oauth2_scheme, get_user_by_id
from src.auth.utils import check_access_permissions
from src.config import settings
from src.database import get_session
from src.exceptions import not_found_exception
from src.tracker.exceptions import not_enough_permissions_exception as tracker_not_enough_permissions_exception


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db_session: Annotated[AsyncSession, Depends(get_session)]):
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


async def check_user_id(user_id: Annotated[UUID, Path()], db_session: Annotated[AsyncSession, Depends(get_session)]):
    user = await get_user_by_id(user_id, db_session)
    if not user:
        raise not_found_exception
    return user


async def check_access(target_user: Annotated[UserInDB, Depends(check_user_id)],
                       current_user: Annotated[UserInDB, Depends(get_current_user)]):
    if not check_access_permissions(current_user, target_user):
        raise tracker_not_enough_permissions_exception
