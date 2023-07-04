from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from api.handlers import create_new_user, delete_user
from db.session import get_session
from models.models import CreateUser, ShowUser, ShowDeletedUser

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/registration", response_model=ShowUser)
async def registration(user: Annotated[CreateUser, Body(title='Registration body')],
                       session: AsyncSession = Depends(get_session)) -> ShowUser:
    return await create_new_user(user, session)


@user_router.delete("/{user_id}", response_model=ShowDeletedUser)
async def registration(user_id: UUID, session: AsyncSession = Depends(get_session)) -> ShowDeletedUser:
    return await delete_user(user_id, session)
