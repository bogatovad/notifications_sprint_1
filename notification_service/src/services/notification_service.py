from contextlib import contextmanager
from sqlalchemy.orm import Session

from db.models import User, Notification
from db.postgres import SessionLocal
from services.base_db_service import BaseDBService


@contextmanager
def service_with_session(session: Session):
    """Возвращает подготовленный сервис."""
    service = NotificationService(session)
    yield service
    service.close()


class NotificationService(BaseDBService):
    """Сервис по работе с моделью Notification."""
    _model = Notification


def get_notification_service() -> NotificationService:
    with service_with_session(SessionLocal()) as service:
        return service