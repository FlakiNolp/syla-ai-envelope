from domain.values.email import Email
from sqlalchemy import select, func

from domain.entities.user import User as DomainUser, User
from infrastructure.repositories.models import User as SQLAlchemyUser
from infrastructure.repositories.base_sqlalchemy_repository import (
    BaseSQLAlchemyRepository,
)
from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.repositories.users.converters import UserConverter


class SQLAlchemyUserRepository(BaseUserRepository, BaseSQLAlchemyRepository):
    async def get_by_email(self, email: Email) -> DomainUser:
        user = (await self._async_transaction.scalars(select(SQLAlchemyUser).filter(SQLAlchemyUser.email == email.as_generic_type()))).one_or_none()
        return None if user is None else UserConverter.convert_from_sqlalchemy_to_entity(user)

    async def add(self, user: User) -> None:
        user = UserConverter.convert_from_entity_to_sqlalchemy(user)
        self._async_transaction.add(user)
