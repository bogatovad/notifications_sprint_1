from contextlib import contextmanager
from sqlalchemy.orm import Session

from db.models import User
from db.postgres import SessionLocal
from services.base_db_service import BaseDBService


@contextmanager
def service_with_session(session: Session):
    """Возвращает подготовленный сервис."""
    service = UserService(session)
    yield service
    service.close()


class UserService(BaseDBService):
    """Сервис по работе с моделью User."""
    _model = User


def get_user_service() -> UserService:
    with service_with_session(SessionLocal()) as service:
        return service