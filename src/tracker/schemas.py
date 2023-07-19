from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

"""Pydantic модели"""


class TasksTypes(str, Enum):
	lab = "Lab"
	coursework = "Coursework"
	report = "Report"
	presentation = "Presentation"
	typical = "Typical"


class Priority(str, Enum):
	low = "Low"
	medium = "Medium"
	high = "High"


class Task(BaseModel):
	id: UUID
	name: str = Field(max_length=100)
	deadline: datetime | None
	description: str | None
	type: TasksTypes | None
	priority: Priority
	status: bool = False
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
	teacher_id: UUID | None
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

	class Congig:
		orm_mode = True


class InnerSubjectTaskResponse(BaseModel):
	id: UUID
	name: str
	deadline: datetime | None
	description: str | None
	type: TasksTypes | None
	priority: Priority
	status: bool

	class Config:
		orm_mode = True


class SubjectResponse(BaseModel):
	id: UUID
	name: str
	course: int | None
	teacher: TeacherResponse | None
	tasks_count: int | None
	tasks: list[InnerSubjectTaskResponse]

	class Config:
		orm_mode = True


class DeleteSubject(BaseModel):
	id: UUID

	class Config:
		orm_mode = True


class UpdateSubject(SubjectResponse):
	pass


class UpdateSubjectRequest(BaseModel):
	name: str | None
	course: int | None
	teacher_id: UUID | None


class InnerTaskSubjectResponse(BaseModel):
	id: UUID
	name: str
	course: int | None
	teacher: TeacherResponse | None

	class Config:
		orm_mode = True


class TaskResponse(BaseModel):
	id: UUID
	name: str
	deadline: datetime | None
	description: str | None
	type: TasksTypes | None
	priority: Priority
	status: bool
	subject: InnerTaskSubjectResponse

	class Config:
		orm_mode = True


class CreateTask(BaseModel):
	name: str = Field(max_length=100)
	deadline: datetime | None
	description: str | None
	type: TasksTypes | None
	priority: Priority
	subject_id: UUID


class DeleteTask(BaseModel):
	id: UUID

	class Config:
		orm_mode = True


class UpdateTaskRequest(BaseModel):
	name: str | None = Field(max_length=100)
	deadline: datetime | None
	description: str | None
	type: TasksTypes | None
	status: bool | None  # Possible that this row drop my nervous system if future
	priority: Priority | None
	subject_id: UUID | None


class UpdateTask(TaskResponse):
	pass


class TeacherSorts(str, Enum):
	by_name = "name"
	by_surname = 'surname'
	by_father_name = 'father_name'


class SubjectSorts(str, Enum):
	by_name = "name"
	by_course = 'course'
	by_tasks_count = 'tasks_count'


class TaskSorts(str, Enum):
	by_name = "name"
	by_deadline = "deadline"
	by_type = "type"
	by_priority = "priority"
	by_status = "status"
