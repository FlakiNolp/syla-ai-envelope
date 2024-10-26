from dataclasses import dataclass

from domain.entities.chat import Chat
from domain.entities.message import Message
from domain.values.id import UUID7
from infrastructure.repositories.messages.base import BaseMessagesRepository
from infrastructure.unit_of_work.base import BaseUnitOfWork
from infrastructure.unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork
from logic.exceptions.chats import ChatNotExistsException
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetHistoryMessages(BaseQuery):
    user_id: str
    chat_id: str


@dataclass(frozen=True)
class GetHistoryMessagesHandler(BaseQueryHandler[GetHistoryMessages, list[Message]]):
    uow: BaseUnitOfWork
    messages: BaseMessagesRepository

    @SQLAlchemyUnitOfWork.provide_async_uow
    async def handle(self, query: GetHistoryMessages) -> list[Chat]:
        user = await self.uow.chats.exists_by_user_id(UUID7(query.user_id), chat_id=UUID7(query.chat_id))
        if user is None:
            raise ChatNotExistsException(query.chat_id)
        return await self.messages.get_all_messages(chat_id=query.chat_id)
