from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from db.postgres import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    

class Notification(Base):
    __tablename__ = "notification"

    template = 
    users = 
    groups =
