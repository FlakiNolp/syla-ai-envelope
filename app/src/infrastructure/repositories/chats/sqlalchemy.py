from domain.values.email import Email
from sqlalchemy import select, func

from domain.entities.user import User as DomainUser
from infrastructure.repositories.models import User as SQLAlchemyUser
from infrastructure.repositories.base_sqlalchemy_repository import (
    BaseSQLAlchemyRepository,
)
from infrastructure.repositories.chats.converters import UserConverter
from app.src.infrastructure.repositories.chats.base import BaseChatRepository


class SQLAlchemyChatRepository(BaseChatRepository, BaseSQLAlchemyRepository):
    ...
