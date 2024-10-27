from domain.values.email import Email
from sqlalchemy import select, func

from domain.entities.user import User as DomainUser, User
from domain.values.id import UUID7
from infrastructure.repositories.models import User as SQLAlchemyUser
from infrastructure.repositories.base_sqlalchemy_repository import (
    BaseSQLAlchemyRepository,
)
from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.repositories.users.converters import UserConverter


class SQLAlchemyUserRepository(BaseUserRepository, BaseSQLAlchemyRepository):
    """
    SQLAlchemy реализация репозитория пользователей
    """
    async def get_by_id(self, user_id: UUID7) -> User | None:
        user = (
            await self._async_transaction.scalars(select(SQLAlchemyUser).filter(SQLAlchemyUser.id == user_id))
        ).one_or_none()
        if user is None:
            return None
        return UserConverter.convert_from_sqlalchemy_to_entity(user)

    async def get_by_email(self, email: Email) -> DomainUser | None:
        user = (
            await self._async_transaction.scalars(
                select(SQLAlchemyUser).filter(SQLAlchemyUser.email == email.as_generic_type())
            )
        ).one_or_none()
        if user is None:
            return None
        return UserConverter.convert_from_sqlalchemy_to_entity(user)
