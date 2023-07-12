from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.tracker.schemas import Teacher
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
