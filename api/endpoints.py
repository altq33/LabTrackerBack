from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.handlers import create_new_user, delete_user, get_user_by_id, update_user
from db.session import get_session
from models.models import CreateUser, ShowUser, ShowDeletedUser, ShowUpdatedUser, UpdateUserRequest

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/registration", response_model=ShowUser)
async def registration(user: Annotated[CreateUser, Body(title='Registration body')],
                       session: AsyncSession = Depends(get_session)) -> ShowUser:
    return await create_new_user(user, session)


@user_router.delete("/{user_id}", response_model=ShowDeletedUser)
async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_session)) -> ShowDeletedUser:
    return await delete_user(user_id, session)


@user_router.get("/{user_id}", response_model=ShowUser)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_session)) -> ShowUser:
    return await get_user_by_id(user_id, session)


@user_router.patch("/{user_id}", response_model=ShowUpdatedUser)
async def update_user_by_id(user_id: UUID, body: UpdateUserRequest, session: AsyncSession = Depends(get_session)) -> ShowUpdatedUser:
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for updating must be passed")
    user = await get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail=f"User with {user_id} id NOT FOUND")
    updated_user = await update_user(user_id, body, session)
    return updated_user
