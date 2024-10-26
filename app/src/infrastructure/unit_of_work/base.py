from abc import ABC, abstractmethod

from infrastructure.repositories.chats.base import BaseChatRepository
from infrastructure.repositories.users.base import BaseUserRepository

class BaseUnitOfWork(ABC):
    users: BaseUserRepository
    chats: BaseChatRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def flush(self, *args):
        raise NotImplementedError
