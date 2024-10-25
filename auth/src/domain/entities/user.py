from dataclasses import dataclass, asdict, field

from domain.entities.base import BaseEntity
from domain.entities.chat import Chat
from domain.values.chat_name import ChatName
from domain.values.email import Email
from domain.values.password import Password, HashedPassword


@dataclass
class User(BaseEntity):
    email: Email
    password: Password | HashedPassword
    chats: set[Chat] = field(default_factory=set)

    def create_chat(self, chat_name: ChatName) -> Chat:
        chat = Chat(user_id=self.id, name=chat_name)
        self.chats.add(chat)
        return chat

    def delete_chat(self, chat: Chat):
        self.chats.remove(chat)
