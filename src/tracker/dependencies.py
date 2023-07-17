from typing import Annotated
from uuid import UUID

from fastapi import Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.auth.schemas import UserInDB
from src.database import get_session
from src.exceptions import not_found_exception
from src.tracker.exceptions import not_enough_permissions_exception
from src.tracker.service import get_teacher_by_id, get_subject_by_id, get_task_by_id
from src.tracker.utils import check_items_access_permissions


async def check_teacher_id(teacher_id: Annotated[UUID, Path()],
                           db_session: Annotated[AsyncSession, Depends(get_session)]):
	teacher = await get_teacher_by_id(teacher_id, db_session)
	if not teacher:
		raise not_found_exception
	return teacher


async def check_subject_id(subject_id: Annotated[UUID, Path()],
                           db_session: Annotated[AsyncSession, Depends(get_session)]):
	subject = await get_subject_by_id(subject_id, db_session)
	if not subject:
		raise not_found_exception
	return subject


async def check_task_id(task_id: Annotated[UUID, Path()], db_session: Annotated[AsyncSession, Depends(get_session)]):
	task = await get_task_by_id(task_id, db_session)
	if not task:
		raise not_found_exception
	return task


async def check_access_to_teachers(current_user: Annotated[UserInDB, Depends(get_current_user)],
                                   teacher=Depends(check_teacher_id)):
	if not check_items_access_permissions(current_user, teacher):
		raise not_enough_permissions_exception


async def check_access_to_tasks(current_user: Annotated[UserInDB, Depends(get_current_user)],
                                task=Depends(check_task_id)):
	if not check_items_access_permissions(current_user, task):
		raise not_enough_permissions_exception


async def check_access_to_subjects(current_user: Annotated[UserInDB, Depends(get_current_user)],
                                   subject=Depends(check_subject_id)):
	if not check_items_access_permissions(current_user, subject):
		raise not_enough_permissions_exception
