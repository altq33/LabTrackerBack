from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext

from src.config import settings


class Hasher:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return Hasher.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_hashed_password(plain_password):
        return Hasher.pwd_context.hash(plain_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret, algorithm=settings.algorithm)
    return encoded_jwt



