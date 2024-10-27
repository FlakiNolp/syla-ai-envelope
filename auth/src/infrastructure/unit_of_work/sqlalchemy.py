from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from infrastructure.repositories.users.sqlalchemy import SQLAlchemyUserRepository
from infrastructure.unit_of_work.base import BaseUnitOfWork


class SQLAlchemyUnitOfWork(BaseUnitOfWork):
    """
    Реализация UOW для SQLAlchemy транзакций
    """
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self._async_session_maker: async_sessionmaker[AsyncSession] = session_maker

    @staticmethod
    def _provide_async_transaction(func):
        """
        Статический метод для опрокидывания в функцию транзакции
        :param func: Функция, в которую будет добавляться транзакция
        :return:
        """
        async def wrapper(self, *args, **kwargs):
            async with self._async_session_maker.begin() as async_transaction:
                return await func(self, *args, **kwargs, async_transaction=async_transaction)

        return wrapper

    @staticmethod
    def provide_async_uow(func):
        """
        Статический метод запуска оборачиваемой функции в контекстном менеджере UOW для управления состоянием транзакции
        :param func: Функция, которая будет оборачиваться
        :return:
        """
        async def wrapper(self, *args, **kwargs):
            async with self.uow:
                return await func(self, *args, **kwargs)

        return wrapper

    @_provide_async_transaction
    async def __aenter__(self, async_transaction: AsyncSession = None):
        """
        Асинхронный контекстный менеджер, который создает репозитории с прокинутыми транзакциями
        :param async_transaction:
        :return:
        """
        self._async_transaction = async_transaction
        self.users = SQLAlchemyUserRepository(self._async_transaction)

    async def __aexit__(self, *args):
        """
        Выход из асинхронного контекстного менеджера с rollback всего незакомиченного
        :param args:
        :return:
        """
        await self.rollback()
        await self._async_transaction.close()

    async def commit(self):
        await self._async_transaction.commit()

    async def rollback(self):
        await self._async_transaction.rollback()

    async def flush(self, *args):
        await self._async_transaction.flush(*args)

    async def begin_nested(self):
        await self._async_transaction.begin_nested()
