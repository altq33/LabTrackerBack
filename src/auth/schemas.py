from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, UUID4

"""Pydantic модели"""


class Roles(str, Enum):
    user = 'User'
    admin = 'Admin'


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example    ":
                {
                 "username": "Faker",
                 "email": "thebestmidlaner@gmail.com",
                 "password": "T1letmeout1234"
                }
        }


class ShowUser(BaseModel):
    username: str
    email: EmailStr
    created: datetime


class UserInDB(ShowUser):
    id: UUID
    hashed_password: str
    roles: list[Roles]


class ShowDeletedUser(BaseModel):
    id: UUID


class ShowUpdatedUser(BaseModel):
    id: UUID


class UpdateUserRequest(BaseModel):
    username: str | None
    email: EmailStr | None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    roles: list[Roles]



