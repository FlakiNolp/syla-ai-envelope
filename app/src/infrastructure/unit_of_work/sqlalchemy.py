from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from infrastructure.repositories.chats.sqlalchemy import SQLAlchemyChatRepository
from infrastructure.repositories.users.sqlalchemy import SQLAlchemyUserRepository

from infrastructure.unit_of_work.base import BaseUnitOfWork


class SQLAlchemyUnitOfWork(BaseUnitOfWork):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self._async_session_maker: async_sessionmaker[AsyncSession] = session_maker

    @staticmethod
    def _provide_async_transaction(func):
        async def wrapper(self, *args, **kwargs):
            async with self._async_session_maker.begin() as async_transaction:
                return await func(self, *args, **kwargs, async_transaction=async_transaction)

        return wrapper

    @_provide_async_transaction
    async def __aenter__(self, async_transaction: AsyncSession = None):
        self._async_transaction = async_transaction
        self.users = SQLAlchemyUserRepository(self._async_transaction)
        self.chats = SQLAlchemyChatRepository(self._async_transaction)

    async def __aexit__(self, *args):
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
