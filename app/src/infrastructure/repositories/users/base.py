import abc
from domain.entities.user import User
from domain.values.email import Email


class BaseUserRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_email(self, email: Email) -> User: raise NotImplementedError
