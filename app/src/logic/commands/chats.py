from dataclasses import dataclass

from domain.entities.chat import Chat
from domain.values.chat_name import ChatName
from domain.values.id import UUID7
from infrastructure.unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork
from domain.entities.access_token import AccessToken
from domain.entities.jwt_payload import JWTPayload
from domain.entities.registration_token import RegistrationToken
from domain.entities.user import User
from domain.values.alg import Alg
from domain.values.email import Email
from domain.values.jwt_header import JWTHeader
from domain.values.password import Password, HashedPassword
from infrastructure.email_service.base import BaseEmailService
from infrastructure.jwt.base import BaseJWT, TokenType
from infrastructure.unit_of_work.base import BaseUnitOfWork
from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.users import UserIdExistsException


@dataclass(frozen=True)
class CreateChat(BaseCommand):
    user_id: str
    chat_name: str


@dataclass(frozen=True)
class CreateChatHandler(CommandHandler[CreateChat, Chat]):
    uow: BaseUnitOfWork

    @SQLAlchemyUnitOfWork.provide_async_uow
    async def handle(self, command: CreateChat) -> Chat:
        user = await self.uow.users.get_by_id(UUID7(command.user_id))
        if user is None:
            raise UserIdExistsException(command.user_id)
        chat = user.create_chat(ChatName(command.chat_name))
        await self.uow.chats.add(chat)
        await self.uow.commit()
        return chat
