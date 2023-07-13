from typing import Sequence
from uuid import UUID

from sqlalchemy import select, RowMapping, Row, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.tracker.schemas import Teacher, CreateTeacher
from src.tracker.models import Teacher as TeacherDB


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


async def delete_teacher_by_id(user_id: UUID, teacher_id: UUID, db_session: AsyncSession):
    pass
