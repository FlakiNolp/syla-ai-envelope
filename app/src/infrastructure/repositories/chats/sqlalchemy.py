from domain.entities.chat import Chat
from domain.values.email import Email
from sqlalchemy import select, func

from domain.values.id import UUID7
from infrastructure.repositories.base_sqlalchemy_repository import (
    BaseSQLAlchemyRepository,
)
from infrastructure.repositories.chats.base import BaseChatRepository
from infrastructure.repositories.chats.converters import ChatConverter
from infrastructure.repositories.models import Chat as SQLAlchemyChat


class SQLAlchemyChatRepository(BaseChatRepository, BaseSQLAlchemyRepository):
    async def add(self, chat: Chat) -> None:
        chat = ChatConverter.convert_from_entity_to_sqlalchemy(chat)
        self._async_transaction.add(chat)

    async def get_chats_by_user_id(self, user_id: UUID7) -> list[Chat]:
        chats = (await self._async_transaction.scalars(select(SQLAlchemyChat).filter(SQLAlchemyChat.user_id == user_id))).unique().all()
        chats = [ChatConverter.convert_from_sqlalchemy_to_entity(chat) for chat in chats]
        return chats
