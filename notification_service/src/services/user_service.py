from db.models import User
from db.postgres import async_session
from fastapi import Depends
from models.events import UserModel
from services.base_db_service import BaseDBService
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class UserService(BaseDBService):
    """Сервис по работе с моделью User."""

    _model = User

    async def find_one(self, **kwargs) -> UserModel:
        result = await self._session.execute(select(self._model).filter_by(**kwargs))
        db_user = result.scalars().all()
        return db_user[0].serialize

    async def get_users(self, user_list: list | None) -> list[UserModel]:
        if not user_list:
            result = await self._session.execute(select(self._model))
        else:
            result = await self._session.execute(
                select(self._model).filter(self._model.id.in_(user_list))
            )
        db_users = result.scalars().all()
        return [item.serialize for item in db_users]


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)
