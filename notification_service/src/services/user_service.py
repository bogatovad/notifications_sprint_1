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

    def find_one(self, **kwargs):
        db_user = self._session.query(self._model).filter_by(**kwargs).first()
        return db_user.serialize

    def get_users(self, user_list):
        if not user_list:
            db_users = self._session.query(self._model).all()
        else:
            db_users = self._session.query(self._model).filter(
                self._model.id.in_(user_list)
            )
        return [item.serialize for item in db_users]


def get_user_service() -> UserService:
    with service_with_session(SessionLocal()) as service:
        return service
