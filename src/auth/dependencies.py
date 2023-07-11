from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import Roles, TokenData
from src.auth.service import get_user_by_username, oauth2_scheme, get_user_by_id
from src.config import settings
from src.database import get_session


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

