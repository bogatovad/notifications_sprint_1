from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import Base

from db.postgres import Base

from db.postgres import Base


class BaseDBService:
    """Базовый класс сервисов."""

    _model = Base

    def __init__(self, session: AsyncSession):
        self._session = session