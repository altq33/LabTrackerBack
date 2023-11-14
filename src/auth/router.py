from datetime import timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, check_user_id, check_access
from src.auth.exceptions import already_busy_exception, incorrect_auth_data_exception
from src.auth.schemas import CreateUser, ShowUser, ShowDeletedUser, ShowUpdatedUser, UpdateUserRequest, Token, UserInDB
from src.auth.service import create_new_user, delete_user_by_id, get_user_by_id, update_user, authenticate_user
from src.auth.utils import create_access_token
from src.config import settings
from src.database import get_session
from src.exceptions import empty_body_exception

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=ShowUser)
async def registration(user: Annotated[CreateUser, Body(title='Registration body')],
                       session: AsyncSession = Depends(get_session)) -> ShowUser:
    new_user = await create_new_user(user, session)
    if not new_user:
        raise already_busy_exception
    return new_user


@router.delete("/{user_id}", response_model=ShowDeletedUser, dependencies=[Depends(check_access)])
async def delete_user(user_id: UUID, session: Annotated[AsyncSession, Depends(get_session)]) -> ShowDeletedUser:
    deleted_user = await delete_user_by_id(user_id, session)
    return deleted_user


@router.get("/me", response_model=ShowUser)
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
):
    return current_user


@router.get("/{user_id}", response_model=ShowUser, dependencies=[Depends(check_user_id)])
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_session)) -> ShowUser:
    user = await get_user_by_id(user_id, session)
    return user


@router.patch("/{user_id}", response_model=ShowUpdatedUser, dependencies=[Depends(check_access)])
async def update_user_by_id(user_id: UUID, body: UpdateUserRequest,
                            session: Annotated[AsyncSession, Depends(get_session)],
                            ) -> ShowUpdatedUser:
    if body.dict(exclude_none=True) == {}:
        raise empty_body_exception
    updated_user = await update_user(user_id, body, session)
    if not updated_user:
        raise already_busy_exception
    return updated_user


@router.post("/auth", response_model=Token)
async def login_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                          session: Annotated[AsyncSession, Depends(get_session)]):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise incorrect_auth_data_exception
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": user.username, "roles": user.roles},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "user": user}


