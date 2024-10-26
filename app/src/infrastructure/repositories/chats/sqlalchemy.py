from domain.values.email import Email
from sqlalchemy import select, func

from infrastructure.repositories.base_sqlalchemy_repository import (
    BaseSQLAlchemyRepository,
)
from app.src.infrastructure.repositories.chats.base import BaseChatRepository


class SQLAlchemyChatRepository(BaseChatRepository, BaseSQLAlchemyRepository):
    ...
