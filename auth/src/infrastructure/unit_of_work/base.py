from abc import ABC, abstractmethod

from infrastructure.repositories.users.base import BaseUserRepository


class BaseUnitOfWork(ABC):
    """
    Базовый класс UOW, который предоставляет интерфейс для работы с ним
    """
    users: BaseUserRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
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
