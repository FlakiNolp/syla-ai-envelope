from motor.core import AgnosticClientSession

from domain.entities.message import Message
from infrastructure.repositories.base_motor_repository import BaseMongoDBRepository
from infrastructure.repositories.messages.base import BaseMessagesRepository
from infrastructure.repositories.messages.converters import MessageConverter


class MongoDBMessagesRepository(BaseMongoDBRepository, BaseMessagesRepository):
    @BaseMongoDBRepository.provide_async_session
    async def add_message(self, message: Message, chat_id: str, async_session: AgnosticClientSession = None):
        await self._collection(chat_id).insert_one(
            MessageConverter.convert_from_entity_to_json(message), session=async_session
        )

    @BaseMongoDBRepository.provide_async_session
    async def get_all_messages(self, chat_id: str, async_session: AgnosticClientSession = None) -> list[Message]:
        messages = await self._collection(chat_id).find({}, session=async_session).to_list()
        return [MessageConverter.convert_from_json_to_entity(message) for message in messages]
