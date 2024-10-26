from dataclasses import dataclass, field

from domain.entities.message import Message
from domain.values.id import UUID7
from domain.entities.base import BaseEntity
from domain.values.chat_name import ChatName


@dataclass
class Chat(BaseEntity):
    user_id: UUID7 | str
    name: ChatName
    messages: set[Message] = field(default_factory=set)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id
