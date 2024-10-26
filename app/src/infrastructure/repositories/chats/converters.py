from domain.entities.chat import Chat as DomainChat
from domain.values.chat_name import ChatName
from infrastructure.repositories.models import Chat


class ChatConverter:
    @classmethod
    def convert_from_sqlalchemy_to_entity(cls, model: Chat) -> DomainChat:
        return DomainChat(
            id=model.id,
            user_id=model.user_id,
            name=ChatName(model.name),
        )

    @classmethod
    def convert_from_entity_to_sqlalchemy(cls, entity: DomainChat) -> Chat:
        return Chat(
            id=entity.id,
            user_id=entity.user_id,
            name=entity.name.as_generic_type(),
        )
