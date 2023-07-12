import uuid
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, Column, UUID, ARRAY, MetaData

from src.auth.schemas import Roles
from src.database import Base

"""DB MODELS"""

metadata = MetaData()


class User(Base):
    __tablename__ = 'users'
    metadata = metadata

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password = Column(
        String(length=1024), nullable=False
    )
    username = Column(String, unique=True, nullable=False)
    created = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    roles = Column(ARRAY(String), nullable=False, default=[Roles.user])