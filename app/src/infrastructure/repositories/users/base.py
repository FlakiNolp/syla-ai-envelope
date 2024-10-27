import abc
from domain.entities.user import User
from domain.values.email import Email
from domain.values.id import UUID7


class BaseUserRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_email(self, email: Email) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    async def add(self, user: User) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, user_id: UUID7) -> User:
        raise NotImplementedError
