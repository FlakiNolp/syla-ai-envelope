import abc
from domain.entities.user import User
from domain.values.email import Email
from domain.values.id import UUID7


class BaseUserRepository(abc.ABC):
    """
    Базовый класс, который предоставляется интерфейс для работы с репозиторием пользователей
    """
    @abc.abstractmethod
    async def get_by_email(self, email: Email) -> User | None:
        """
        Получить пользователя по email
        :param email: Почта пользователя
        :return: Сущность пользователя или ничего
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, user_id: UUID7) -> User | None:
        """
        Получить пользователя по id
        :param user_id: Id пользователя
        :return: Сущность пользователя или ничего
        """
        raise NotImplementedError
