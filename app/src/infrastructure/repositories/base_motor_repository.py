from motor.core import AgnosticClientSession, AgnosticCollection, AgnosticDatabase, AgnosticClient


class BaseMongoDBRepository:
    def __init__(self, mongodb_client: AgnosticClient, db_name: str) -> None:
        self.mongo_db_client: AgnosticClient = mongodb_client
        self.mongo_db_db_name: str = db_name

    def _db(self) -> AgnosticDatabase:
        return self.mongo_db_client[self.mongo_db_db_name]

    def _collection(self, collection_name: str) -> AgnosticCollection:
        return self.mongo_db_client[self.mongo_db_db_name][collection_name]

    @staticmethod
    def provide_async_session(func):
        async def wrapper(self, *args, **kwargs):
            async with await self.mongo_db_client.start_session() as async_session:
                print(type(async_session), async_session.has_ended)
                async_session: AgnosticClientSession
                return await func(self, *args, **kwargs, async_session=async_session)

        return wrapper
