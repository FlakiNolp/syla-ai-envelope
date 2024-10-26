from domain.entities.message import Message as DomainMessage
from domain.values.id import UUID7


class MessageConverter:
    @classmethod
    def convert_from_json_to_entity(cls, model: dict) -> DomainMessage:
        return DomainMessage(id=model["id"], chat_id=model["chat_id"], text=model["text"], author=model["author"])

    @classmethod
    def convert_from_entity_to_json(cls, entity: DomainMessage) -> dict:
        return entity.model_dump()
