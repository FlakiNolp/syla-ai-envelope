import abc

from domain.entities.message import Message


class BaseMessagesRepository(abc.ABC):
    @abc.abstractmethod
    async def add_message(self, message: Message, chat_id: str): raise NotImplementedError
    @abc.abstractmethod
    async def get_all_messages(self, chat_id: str): raise NotImplementedError