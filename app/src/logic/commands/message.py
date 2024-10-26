from dataclasses import dataclass

from domain.entities.chat import Chat
from domain.entities.message import Message
from domain.values.author import Author
from domain.values.chat_name import ChatName
from domain.values.id import UUID7
from infrastructure.integrations.rag.base import BaseRag
from infrastructure.repositories.base_motor_repository import BaseMongoDBRepository
from infrastructure.repositories.messages.base import BaseMessagesRepository
from infrastructure.unit_of_work.mongodb import MongoDBUnitOfWork
from infrastructure.unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork
from infrastructure.unit_of_work.base import BaseUnitOfWork
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class ReceivedMessage(BaseCommand):
    text: str
    user_id: str
    chat_id: str


@dataclass(frozen=True)
class ReceivedMessageHandler(CommandHandler[ReceivedMessage, Message]):
    uow: BaseUnitOfWork
    messages: BaseMessagesRepository
    # rag: BaseRag

    @SQLAlchemyUnitOfWork.provide_async_uow
    async def handle(self, command: ReceivedMessage) -> Message:
        if not await self.uow.chats.exists_by_user_id(user_id=UUID7(command.user_id), chat_id=UUID7(command.chat_id)):
            raise
        message = Message(chat_id=UUID7(command.chat_id), text=command.text, author=Author.user)
        await self.messages.add_message(message, chat_id=command.chat_id)
        return message

