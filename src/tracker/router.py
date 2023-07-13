from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user as auth_get_current_user
from src.auth.schemas import UserInDB
from src.database import get_session
from src.tracker.schemas import TeacherResponse, Teacher, CreateTeacher, DeleteTeacher, SubjectResponce, CreateSubject
from src.tracker.service import get_teacher_by_id, get_teachers_by_user_id, create_teacher_by_user_id, \
    delete_teacher_by_id, create_subject_by_user_id
from src.tracker.utils import check_items_access_permissions

teachers_router = APIRouter(prefix="/teachers", tags=["teachers"])
subjects_router = APIRouter(prefix="/subjects", tags=["subjects"])


"""Teachers CRUD"""


@teachers_router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher(teacher_id: UUID, session: Annotated[AsyncSession, Depends(get_session)],
                      current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
    teacher = await get_teacher_by_id(teacher_id, session)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"teacher with {teacher_id} id NOT FOUND")
    if not check_items_access_permissions(current_user, teacher):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return teacher


@teachers_router.get("/", response_model=list[TeacherResponse])
async def get_all_teachers(session: Annotated[AsyncSession, Depends(get_session)],
                           current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
    teachers = await get_teachers_by_user_id(current_user.id, session)
    if not teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="teachers NOT FOUND")
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"teacher with {teacher_id} id NOT FOUND")
    if not check_items_access_permissions(current_user, teacher):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    deleted_teacher = await delete_teacher_by_id(teacher_id, session)
    return deleted_teacher


"""Subjects CRUD"""


@subjects_router.post("/", response_model=SubjectResponce)
async def create_subject(subject: CreateSubject, session: Annotated[AsyncSession, Depends(get_session)],
                         current_user: Annotated[UserInDB, Depends(auth_get_current_user)]):
    created_subject = await create_subject_by_user_id(current_user.id, subject, session)

    return created_subject
