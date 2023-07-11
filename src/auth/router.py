from datetime import timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.auth.schemas import CreateUser, ShowUser, ShowDeletedUser, ShowUpdatedUser, UpdateUserRequest, Token, UserInDB
from src.auth.service import create_new_user, delete_user_by_id, get_user_by_id, update_user, authenticate_user
from src.auth.utils import create_access_token, check_access_permissions
from src.config import settings
from src.database import get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=ShowUser)
async def registration(user: Annotated[CreateUser, Body(title='Registration body')],
                       session: AsyncSession = Depends(get_session)) -> ShowUser:
    new_user = await create_new_user(user, session)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username already busy")
    return new_user


@router.delete("/{user_id}", response_model=ShowDeletedUser)
async def delete_user(user_id: UUID, session: Annotated[AsyncSession, Depends(get_session)],
                      current_user: Annotated[UserInDB, Depends(get_current_user)]) -> ShowDeletedUser:
    target_user = await get_user_by_id(user_id, session)
    if not target_user:
        raise HTTPException(status_code=404, detail=f"user with {user_id} id NOT FOUND")
    if check_access_permissions(current_user, target_user):
        deleted_user = await delete_user_by_id(user_id, session)
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return deleted_user


@router.get("/me", response_model=ShowUser)
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
):
    return current_user


@router.get("/{user_id}", response_model=ShowUser)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_session)) -> ShowUser:
    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail=f"user with {user_id} id NOT FOUND")
    return user


@router.patch("/{user_id}", response_model=ShowUpdatedUser)
async def update_user_by_id(user_id: UUID, body: UpdateUserRequest,
                            session: Annotated[AsyncSession, Depends(get_session)],
                            current_user: Annotated[UserInDB, Depends(get_current_user)]
                            ) -> ShowUpdatedUser:
    target_user = await get_user_by_id(user_id, session)
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {user_id} id NOT FOUND")
    if check_access_permissions(current_user, target_user):
        if body.dict(exclude_none=True) == {}:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="At least one parameter for updating must be passed")
        updated_user = await update_user(user_id, body, session)
        if not updated_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username already busy")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")
    return updated_user


@router.post("/auth", response_model=Token)
async def login_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                          session: Annotated[AsyncSession, Depends(get_session)]):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": user.username, "roles": user.roles},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


