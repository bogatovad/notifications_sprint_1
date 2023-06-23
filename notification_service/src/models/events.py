from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from .base_model import ORJSONBaseModel


class UserModel(ORJSONBaseModel):
    login: str
    email: str


class NotificationType(str, Enum):
    single = "single"
    group = "group"
    all = 'all'


class EventType(str, Enum):
    welcome = "welcome"
    notice = "notice"


class BaseEventModel(ORJSONBaseModel):
    created_at: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


class RequestEventModel(BaseEventModel):
    receiver: str | list
    name: EventType
    type: NotificationType
    context: dict


class ResponseModel(BaseEventModel):
    email: str
    event_type: str
    context: dict
