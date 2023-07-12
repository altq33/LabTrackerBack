import uuid

from sqlalchemy import String, TIMESTAMP, Column, UUID, MetaData, Text, ForeignKey, SmallInteger

from src.database import Base

"""DB MODELS"""

metadata = MetaData()


class Task(Base):
    __tablename__ = 'tasks'
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(length=100), nullable=False)
    deadline = Column(TIMESTAMP, default=None)
    description = Column(Text, default=None)
    type = Column(String, default=None)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)


class Teacher(Base):
    __tablename__ = 'teachers'
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(length=100), nullable=False)
    surname = Column(String(length=100), nullable=False)
    father_name = Column(String(length=100), nullable=True, default=None)
    phone_number = Column(Text, default=None)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)


class Subject(Base):
    __tablename__ = 'subjects'
    metadata = metadata
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(length=100), nullable=False)
    course = Column(SmallInteger, default=None)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
