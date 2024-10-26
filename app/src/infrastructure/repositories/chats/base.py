import abc

from domain.entities.chat import Chat
from domain.entities.user import User
from domain.values.email import Email
from domain.values.id import UUID7


class BaseChatRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, chat: Chat) -> None: raise NotImplementedError
    @abc.abstractmethod
    async def get_chats_by_user_id(self, user_id: UUID7) -> list[Chat]: raise NotImplementedError
