from typing import Sequence
from uuid import UUID

from sqlalchemy import select, RowMapping, Row, insert, delete, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.tracker.schemas import Teacher, CreateTeacher, CreateSubject, TeacherResponse, SubjectResponse, \
	UpdateSubjectRequest, CreateTask, UpdateTaskRequest
from src.tracker.models import Teacher as TeacherDB
from src.tracker.models import Subject as SubjectDB
from src.tracker.models import Task as TaskDB


async def get_teacher_by_id(teacher_id: UUID, db_session: AsyncSession) -> Teacher | None:
	query = select(TeacherDB).where(TeacherDB.id == teacher_id)
	res = await db_session.execute(query)
	teacher_row = res.fetchone()
	if teacher_row:
		return Teacher(id=teacher_row[0].id,
		               name=teacher_row[0].name,
		               surname=teacher_row[0].surname,
		               father_name=teacher_row[0].father_name,
		               phone_number=teacher_row[0].phone_number,
		               user_id=teacher_row[0].user_id)


async def get_teachers_by_user_id(user_id: UUID, db_session: AsyncSession) -> Sequence[Row | RowMapping] | None:
	query = select(TeacherDB).where(TeacherDB.user_id == user_id)
	res = await db_session.execute(query)
	teachers_rows = res.scalars().fetchall()
	if teachers_rows:
		return teachers_rows


async def create_teacher_by_user_id(user_id: UUID, teacher: CreateTeacher, db_session: AsyncSession):
	query = insert(TeacherDB).values(**teacher.dict(), user_id=user_id).returning(TeacherDB)
	res = await db_session.execute(query)
	await db_session.commit()
	teacher_row = res.scalars().one()
	return teacher_row


async def delete_teacher_by_id(teacher_id: UUID, db_session: AsyncSession):
	query = delete(TeacherDB).where(TeacherDB.id == teacher_id).returning(TeacherDB)
	res = await db_session.execute(query)
	await db_session.commit()
	deleted_teacher_row = res.scalars().one()
	if deleted_teacher_row:
		return deleted_teacher_row


async def create_subject_by_user_id(user_id: UUID, subject: CreateSubject, db_session: AsyncSession):
	query = insert(SubjectDB).values(**subject.dict(), user_id=user_id).returning(SubjectDB)

	res = await db_session.execute(query)
	await db_session.commit()
	subject_row = res.scalars().one()

	query = select(SubjectDB).where(SubjectDB.id == subject_row.id)
	res = await db_session.execute(query)
	subject_row = res.scalars().one()
	return subject_row


async def get_subjects_by_user_id(user_id: UUID, db_session: AsyncSession) -> Sequence[Row | RowMapping] | None:
	query = select(SubjectDB).where(SubjectDB.user_id == user_id)
	res = await db_session.execute(query)
	subjects_rows = res.scalars().all()
	if subjects_rows:
		return subjects_rows


async def get_subject_by_id(subject_id, db_session: AsyncSession) -> Row | RowMapping | None:
	query = select(SubjectDB).where(SubjectDB.id == subject_id)
	res = await db_session.execute(query)
	subject_row = res.scalars().one_or_none()
	if subject_row:
		return subject_row


async def delete_subject_by_id(subject_id: UUID, db_session: AsyncSession):
	query = delete(SubjectDB).where(SubjectDB.id == subject_id).returning(SubjectDB)
	res = await db_session.execute(query)
	await db_session.commit()
	deleted_subject_row = res.scalars().one()
	if deleted_subject_row:
		return deleted_subject_row


async def update_subject_by_id(subject_id: UUID, body: UpdateSubjectRequest, db_session: AsyncSession):
	query = update(SubjectDB).where(SubjectDB.id == subject_id)\
			.values(**body.dict(exclude_none=True))\
			.returning(SubjectDB)
	res = await db_session.execute(query)
	updated_subject_row = res.scalars().one()
	await db_session.refresh(updated_subject_row)
	await db_session.commit()
	return updated_subject_row


async def create_task_by_user_id(user_id: UUID, task: CreateTask, db_session: AsyncSession):
	query = insert(TaskDB).values(**task.dict(), user_id=user_id).returning(TaskDB)
	res = await db_session.execute(query)
	await db_session.commit()
	teacher_row = res.scalars().one()
	return teacher_row


async def get_tasks_by_user_id(user_id: UUID, db_session: AsyncSession) -> Sequence[Row | RowMapping] | None:
	query = select(TaskDB).where(TaskDB.user_id == user_id)
	res = await db_session.execute(query)
	tasks_rows = res.scalars().all()
	if tasks_rows:
		return tasks_rows


async def get_task_by_id(task_id, db_session: AsyncSession) -> Row | RowMapping | None:
	query = select(TaskDB).where(TaskDB.id == task_id)
	res = await db_session.execute(query)
	task_row = res.scalars().one_or_none()
	if task_row:
		return task_row


async def delete_task_by_id(task_id: UUID, db_session: AsyncSession):
	query = delete(TaskDB).where(TaskDB.id == task_id).returning(TaskDB)
	res = await db_session.execute(query)
	await db_session.commit()
	deleted_task_row = res.scalars().one()
	if deleted_task_row:
		return deleted_task_row


async def update_task_by_id(task_id: UUID, body: UpdateTaskRequest, db_session: AsyncSession):
	query = update(TaskDB).where(TaskDB.id == task_id)\
			.values(**body.dict(exclude_none=True))\
			.returning(TaskDB)
	res = await db_session.execute(query)
	updated_task_row = res.scalars().one()
	await db_session.refresh(updated_task_row)
	await db_session.commit()   
	return updated_task_row
