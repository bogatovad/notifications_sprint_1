from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db.postgres import Base
from models.events import UserModel


class User(Base):
    __tablename__ = "auth_user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    username = Column(String, unique=True, nullable=False)
    email = Column(String(255), unique=True)
    
    @property
    def serialize(self):
        return UserModel(login=self.username, email=self.email)
    
    __table_args__ = {"schema": "public"}
