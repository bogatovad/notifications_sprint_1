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


class RequestEventModel(ORJSONBaseModel):
    receiver: str | list
    event_type: EventType
    event_name: str #название шаблона
    type: NotificationType
    context: dict


class ResponseModel(ORJSONBaseModel):
    email: str
    event_type: str
    context: dict
