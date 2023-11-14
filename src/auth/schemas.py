from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, UUID4, Field

"""Pydantic модели"""


class Roles(str, Enum):
    user = 'User'
    admin = 'Admin'


class CreateUser(BaseModel):
    username: str = Field(min_length=4, max_length=100, regex=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(min_length=10, max_length=500,
                          regex=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$")

    class Config:
        schema_extra = {
            "example":
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
    username: str
    email: EmailStr
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
    user: ShowUser


class TokenData(BaseModel):
    username: str | None = None
    roles: list[Roles]



