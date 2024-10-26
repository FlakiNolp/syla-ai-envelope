from domain.entities.message import Message
from infrastructure.repositories.base_motor_repository import BaseMongoDBRepository
from infrastructure.repositories.messages.base import BaseMessagesRepository


class MongoDBMessagesRepository(BaseMongoDBRepository, BaseMessagesRepository):
    @BaseMongoDBRepository.provide_async_session
    async def add_message(self, message: Message, chat_id: str, async_session):
        print(message.model_dump(), async_session.has_ended)
        await self._collection(chat_id).insert_one(message.model_dump(), session=async_session)

