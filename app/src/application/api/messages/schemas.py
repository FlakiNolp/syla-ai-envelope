from typing import Annotated

from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

from domain.entities.chat import Chat
from domain.entities.message import Message
from domain.values.author import Author


class JSONMessage(BaseModel):
    id: str = Field(...)
    chat_id: str = Field(...)
    author: Author = Field(..., alias="author")
    text: str = Field(..., alias="text")
    documents: list[str] | None = Field(None, alias="documents")

    @classmethod
    def from_entity(cls, message: Message) -> "JSONMessage":
        return cls(**message.model_dump())


class ReceivedMessageRequestSchema(BaseModel):
    message: str
    chat_id: str = Field(..., alias="chat-id")


class ReceivedMessageResponseSchema(BaseModel):
    message: JSONMessage

    @classmethod
    def from_entity(cls, message: Message) -> 'ReceivedMessageResponseSchema':
        return cls(message=JSONMessage(message_id=str(message.id), chat_id=str(message.chat_id), author=message.author, text=message.text, documents=message.documents))
