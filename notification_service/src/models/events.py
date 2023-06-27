from enum import Enum
from uuid import UUID, uuid4

from .base_model import ORJSONBaseModel


class UserModel(ORJSONBaseModel):
    id: UUID = uuid4()
    username: str
    email: str


class NotificationType(str, Enum):
    single = "personal"
    group = "group"
    all = "all"


class RequestEventModel(ORJSONBaseModel):
    receiver: str | list
    event_type: str
    event_name: str  # название шаблона
    type: NotificationType
    context: dict


class ResponseModel(ORJSONBaseModel):
    email: str
    event_type: str
    context: dict
