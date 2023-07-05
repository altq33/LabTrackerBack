from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, UUID4

"""Pydantic модели"""


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": [
                {
                 "username": "Faker",
                 "email": "thebestmidlaner@gmail.com",
                 "password": "T1letmeout1234"
                 }
            ]
        }


class ShowUser(BaseModel):
    username: str
    email: EmailStr
    created: datetime


class ShowDeletedUser(BaseModel):
    id: UUID


class ShowUpdatedUser(BaseModel):
    id: UUID


class UpdateUserRequest(BaseModel):
    username: str | None
    email: EmailStr | None
