from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, UUID4, Field

"""Pydantic модели"""


class TasksTypes(str, Enum):
	lab = "Lab"
	coursework = "Coursework"
	report = "Report"
	presentation = "Presentation"
	typical = "Typical"


class Priority(str, Enum):
	standart = "Standart"
	meduim = "Meduim"
	high = "High"


class Task(BaseModel):
	id: UUID
	name: str = Field(max_length=100)
	deadline: datetime | None
	description: str | None
	type: TasksTypes | None
	priority: Priority
	user_id: UUID
	subject_id: UUID


class Teacher(BaseModel):
	id: UUID
	name: str
	surname: str
	father_name: str | None
	phone_number: str | None
	user_id: UUID


class Subject(BaseModel):
	id: UUID
	name: str
	course: int | None
	teacher_id: UUID
	user_id: UUID


class TeacherResponse(BaseModel):
	id: UUID
	name: str
	surname: str
	father_name: str | None
	phone_number: str | None

	class Config:
		orm_mode = True


class CreateTeacher(BaseModel):
	name: str = Field(max_length=100)
	surname: str = Field(max_length=100)
	father_name: str | None = Field(max_length=100)
	phone_number: str | None = Field(regex=r"^(?:\+7|8)?9\d{9}$")


class DeleteTeacher(BaseModel):
	id: UUID

	class Config:
		orm_mode = True


class CreateSubject(BaseModel):
	name: str = Field(max_length=100, min_length=3)
	course: int | None = Field(gt=0, lt=9)
	teacher_id: UUID


class SubjectResponce(BaseModel):
	name: str
	course: int | None
	teacher: TeacherResponse

	class Congig:
		orm_mode = True

