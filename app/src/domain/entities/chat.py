from dataclasses import dataclass

import uuid6
from domain.entities.base import BaseEntity
from domain.values.chat_name import ChatName


@dataclass
class Chat(BaseEntity):
    user_id: uuid6.UUID
    name: ChatName

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id