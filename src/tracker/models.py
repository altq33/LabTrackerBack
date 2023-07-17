import uuid

from sqlalchemy import String, TIMESTAMP, Column, UUID, MetaData, Text, ForeignKey, SmallInteger, Boolean
from sqlalchemy.orm import relationship

from src.auth.models import User
from src.database import Base

"""DB MODELS"""

metadata = MetaData()


class Task(Base):
    __tablename__ = 'tasks'
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(length=100), nullable=False)
    deadline = Column(TIMESTAMP(timezone=True), default=None)
    description = Column(Text, default=None)
    type = Column(String, default=None)
    priority = Column(String, default="Standart")
    status = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete='CASCADE', ), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    subject = relationship("Subject", back_populates="tasks", lazy="selectin")


class Teacher(Base):
    __tablename__ = 'teachers'
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(length=100), nullable=False)
    surname = Column(String(length=100), nullable=False)
    father_name = Column(String(length=100), nullable=True, default=None)
    phone_number = Column(Text, default=None)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = 'subjects'
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(length=100), nullable=False)
    course = Column(SmallInteger, default=None)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey('teachers.id', ondelete='SET NULL'))
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    teacher = relationship("Teacher", back_populates="subjects", lazy="selectin")
    tasks = relationship("Task", back_populates="subject", lazy="selectin")
