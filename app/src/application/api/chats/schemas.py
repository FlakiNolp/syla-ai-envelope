from typing import Annotated
from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

from domain.entities.chat import Chat


class CreateChatRequestSchema(BaseModel):
    chat_name: str = Field(alias="chat-name")


class CreateChatResponseSchema(BaseModel):
    chat_id: str = Field(alias="chat-id")

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return cls(chat_id=str(chat.id))


class JSONChat(BaseModel):
    chat_id: str = Field()
    chat_name: str = Field()

    @classmethod
    def from_entity(cls, chat: Chat) -> 'JSONChat':
        return cls(chat_id=str(chat.id), chat_name=chat.name.as_generic_type())


class GetChatsResponseSchema(BaseModel):
    chats: list[JSONChat]

    @classmethod
    def from_entity(cls, chats: list[Chat]) -> 'GetChatsResponseSchema':
        return cls(chats=[JSONChat.from_entity(chat) for chat in chats])
