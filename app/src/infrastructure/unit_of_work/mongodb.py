from typing import override

from motor.core import AgnosticClient, AgnosticClientSession, _MotorTransactionContext

from infrastructure.repositories.messages.mongodb import MongoDBMessagesRepository
from infrastructure.unit_of_work.base import BaseUnitOfWork


class MongoDBUnitOfWork(BaseUnitOfWork):
    def __init__(self, async_client: AgnosticClient, db_name: str):
        self._mongo_db_client: AgnosticClient = async_client
        self._db_name = db_name

    @staticmethod
    def _provide_async_session(func):
        async def wrapper(self, *args, **kwargs):
            async with await self._mongo_db_client.start_session() as async_session:
                print(type(async_session), async_session.has_ended)
                async_session: AgnosticClientSession
                async with async_session.start_transaction() as async_transaction:
                    async_transaction: _MotorTransactionContext
                    print(type(async_transaction), async_session.__dict__)
                    return await func(self, *args, **kwargs, async_transaction=async_session)

        return wrapper

    # @staticmethod
    # def provide_async_uow(db_name: str):
    #     def decorator(func):
    #         @functools.wraps(func)
    #         async def wrapper(self, *args, **kwargs):
    #             async with self.uow:
    #                 return await func(self, db_name, *args, **kwargs)
    #
    #         return wrapper
    #     return decorator

    @staticmethod
    def provide_async_uow(func):
        async def wrapper(self, *args, **kwargs):
            async with self.uow_mongodb:
                return await func(self, *args, **kwargs)

        return wrapper

    @_provide_async_session
    async def __aenter__(self, async_transaction: AgnosticClientSession = None):
        self._async_transaction = async_transaction
        self.messages = MongoDBMessagesRepository(async_transaction=self._async_transaction, mongodb_client=self._mongo_db_client, db_name=self._db_name)
        return self

    async def __aexit__(self, *args):
        pass

    async def commit(self):
        await self._async_transaction.commit_transaction()

    async def rollback(self):
        raise NotImplementedError

    async def flush(self, *args):
        raise NotImplementedError

    async def begin_nested(self):
        raise NotImplementedError
