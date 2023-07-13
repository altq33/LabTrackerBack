from typing import Sequence
from uuid import UUID

from sqlalchemy import select, RowMapping, Row, insert, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.tracker.schemas import Teacher, CreateTeacher, CreateSubject, TeacherResponse, SubjectResponce
from src.tracker.models import Teacher as TeacherDB
from src.tracker.models import Subject as SubjectDB


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
	subject_row.teacher = TeacherResponse.from_orm(subject_row.teacher)
	subject_row = SubjectResponce.from_orm(subject_row)
	return subject_row
