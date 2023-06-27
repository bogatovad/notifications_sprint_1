from db.postgres import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session


class BaseDBService:
    """Базовый класс сервисов."""

    _model = Base

    def __init__(self, session: AsyncSession):
        self._session = session
