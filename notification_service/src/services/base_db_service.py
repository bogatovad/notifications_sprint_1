from sqlalchemy.orm import Session

from db.postgres import Base


class BaseDBService:
    """Базовый класс сервисов."""

    _model = Base

    def __init__(self, session: Session) -> None:
        self._session = session

    def close(self) -> None:
        """Завершает работу сервиса."""
        self._session.close()
