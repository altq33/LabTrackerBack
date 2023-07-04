from pydantic import BaseModel, EmailStr

"""Pydantic модели"""

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
