import datetime
from fastapi import Query
from pydantic import BaseModel, Field

from domain.entities.message import Message
from domain.values.author import Author


class JSONMessage(BaseModel):
    id: str = Field(...)
    chat_id: str = Field(...)
    author: Author = Field(...)
    text: str = Field(...)
    documents: list[str] | None = Field(None)
    timestamp: datetime.datetime

    @classmethod
    def from_entity(cls, message: Message) -> "JSONMessage":
        return cls(**message.model_dump(uuid_conversation=True))


class ReceivedMessageRequestSchema(BaseModel):
    message: str
    chat_id: str = Field(...)


class GetHistoryRequestSchema(BaseModel):
    chat_id: str = Query(...)


class GetHistoryResponseSchema(BaseModel):
    messages: list[JSONMessage]

    @classmethod
    def from_entity(cls, messages: list[Message]) -> "GetHistoryResponseSchema":
        return cls(messages=[JSONMessage.from_entity(message) for message in messages])
