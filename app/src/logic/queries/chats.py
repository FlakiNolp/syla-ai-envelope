from dataclasses import dataclass

from domain.entities.chat import Chat
from domain.values.id import UUID7
from infrastructure.unit_of_work.base import BaseUnitOfWork
from infrastructure.unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork
from logic.exceptions.users import UserIdExistsException
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetChats(BaseQuery):
    user_id: str


@dataclass(frozen=True)
class GetChatsHandler(BaseQueryHandler[GetChats, list[Chat]]):
    uow: BaseUnitOfWork

    @SQLAlchemyUnitOfWork.provide_async_uow
    async def handle(self, query: GetChats) -> list[Chat]:
        user = await self.uow.users.get_by_id(UUID7(query.user_id))
        if user is None:
            raise UserIdExistsException(query.user_id)
        chats = await self.uow.chats.get_chats_by_user_id(UUID7(query.user_id))
        return chats
