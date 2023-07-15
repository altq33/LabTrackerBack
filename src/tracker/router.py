from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user as auth_get_current_user
from src.exceptions import not_found_exception, empty_body_exception
from src.auth.schemas import UserInDB
from src.database import get_session
from src.tracker.exceptions import not_enough_permissions_exception
from src.tracker.schemas import TeacherResponse, Teacher, CreateTeacher, DeleteTeacher, SubjectResponse, CreateSubject, \
	DeleteSubject, UpdateSubject, UpdateSubjectRequest, CreateTask, TaskResponse, DeleteTask, UpdateTaskRequest, \
	UpdateTask
from src.tracker.service import get_teacher_by_id, get_teachers_by_user_id, create_teacher_by_user_id, \
	delete_teacher_by_id, create_subject_by_user_id, get_subjects_by_user_id, get_subject_by_id, delete_subject_by_id, \
	update_subject_by_id, create_task_by_user_id, get_tasks_by_user_id, get_task_by_id, delete_task_by_id, \
	update_task_by_id
from src.tracker.utils import check_items_access_permissions

teachers_router = APIRouter(prefix="/teachers", tags=["teachers"])
subjects_router = APIRouter(prefix="/subjects", tags=["subjects"])
tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])

"""Teachers CRUD"""


@teachers_router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher(teacher_id: UUID, session: Annotated[AsyncSession, Depends(get_session)],
                      current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	teacher = await get_teacher_by_id(teacher_id, session)
	if not teacher:
		raise not_found_exception
	if not check_items_access_permissions(current_user, teacher):
		raise not_enough_permissions_exception
	return teacher


@teachers_router.get("/", response_model=list[TeacherResponse])
async def get_all_teachers(session: Annotated[AsyncSession, Depends(get_session)],
                           current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	teachers = await get_teachers_by_user_id(current_user.id, session)
	if not teachers:
		raise not_found_exception
	return teachers


@teachers_router.post("/", response_model=TeacherResponse)
async def create_teacher(teacher: CreateTeacher, session: Annotated[AsyncSession, Depends(get_session)],
                         current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	created_teacher = await create_teacher_by_user_id(current_user.id, teacher, session)
	return created_teacher


@teachers_router.delete("/{teacher_id}", response_model=DeleteTeacher)
async def delete_teacher(teacher_id: UUID, session: Annotated[AsyncSession, Depends(get_session)],
                         current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	teacher = await get_teacher_by_id(teacher_id, session)
	if not teacher:
		raise not_found_exception
	if not check_items_access_permissions(current_user, teacher):
		raise not_enough_permissions_exception
	deleted_teacher = await delete_teacher_by_id(teacher_id, session)
	return deleted_teacher


"""Subjects CRUD"""


@subjects_router.post("/", response_model=SubjectResponse)
async def create_subject(subject: CreateSubject, session: Annotated[AsyncSession, Depends(get_session)],
                         current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	created_subject = await create_subject_by_user_id(current_user.id, subject, session)
	return created_subject


@subjects_router.get("/", response_model=list[SubjectResponse])
async def get_all_subjects(session: Annotated[AsyncSession, Depends(get_session)],
                           current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	subjects = await get_subjects_by_user_id(current_user.id, session)
	if not subjects:
		raise not_found_exception
	return subjects


@subjects_router.get("/{subject_id}", response_model=SubjectResponse)
async def get_subject(subject_id: UUID, session: Annotated[AsyncSession, Depends(get_session)],
                      current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	subject = await get_subject_by_id(subject_id, session)
	if not subject:
		raise not_found_exception
	if not check_items_access_permissions(current_user, subject):
		raise not_enough_permissions_exception
	return subject


@subjects_router.delete("/{subject_id}", response_model=DeleteSubject)
async def delete_subject(subject_id: UUID, session: Annotated[AsyncSession, Depends(get_session)],
                         current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	subject = await get_subject_by_id(subject_id, session)
	if not subject:
		raise not_found_exception
	if not check_items_access_permissions(current_user, subject):
		raise not_enough_permissions_exception
	deleted_subject = await delete_subject_by_id(subject_id, session)
	return deleted_subject


@subjects_router.patch("/{subject_id}", response_model=UpdateSubject)
async def update_subject(subject_id: UUID,
                         body: UpdateSubjectRequest,
                         session: Annotated[AsyncSession, Depends(get_session)],
                         current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	subject = await get_subject_by_id(subject_id, session)
	if not subject:
		raise not_found_exception
	if not check_items_access_permissions(current_user, subject):
		raise not_enough_permissions_exception
	if body.dict(exclude_none=True) == {}:
		raise empty_body_exception
	updated_subject = await update_subject_by_id(subject_id, body, session)
	return updated_subject


@tasks_router.post("/", response_model=TaskResponse)
async def create_task(task: CreateTask, session: Annotated[AsyncSession, Depends(get_session)],
                      current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	created_task = await create_task_by_user_id(current_user.id, task, session)
	return created_task


@tasks_router.get("/", response_model=list[TaskResponse])
async def get_all_tasks(session: Annotated[AsyncSession, Depends(get_session)],
                        current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	tasks = await get_tasks_by_user_id(current_user.id, session)
	if not tasks:
		raise not_found_exception
	return tasks


@tasks_router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID, session: Annotated[AsyncSession, Depends(get_session)],
                      current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	task = await get_task_by_id(task_id, session)
	if not task:
		raise not_found_exception
	if not check_items_access_permissions(current_user, task):
		raise not_enough_permissions_exception
	return task


@tasks_router.delete("/{task_id}", response_model=DeleteTask)
async def delete_subject(task_id: UUID, session: Annotated[AsyncSession, Depends(get_session)],
                         current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	task = await get_task_by_id(task_id, session)
	if not task:
		raise not_found_exception
	if not check_items_access_permissions(current_user, task):
		raise not_enough_permissions_exception
	deleted_task = await delete_task_by_id(task_id, session)
	return deleted_task


@tasks_router.patch("/{task_id}", response_model=UpdateTask)
async def update_subject(task_id: UUID,
                         body: UpdateTaskRequest,
                         session: Annotated[AsyncSession, Depends(get_session)],
                         current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
	task = await get_task_by_id(task_id, session)
	if not task:
		raise not_found_exception
	if not check_items_access_permissions(current_user, task):
		raise not_enough_permissions_exception
	if body.dict(exclude_none=True) == {}:
		raise empty_body_exception
	updated_task = await update_task_by_id(task_id, body, session)
	return updated_task
