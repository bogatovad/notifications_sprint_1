from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .base_model import ORJSONBaseModel


class UserModel(ORJSONBaseModel):
    name: str
    email: str


class Type(str, Enum):
    single = "single"
    group = "group"


class BaseEventModel(ORJSONBaseModel):
    created_at: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class RequestEventModel(BaseEventModel):
    receiver: str | list
    name: str
    type: Type
    body: dict