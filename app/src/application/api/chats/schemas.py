from typing import Annotated
from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from domain.entities.chat import Chat


class CreateChatRequestSchema(BaseModel):
    chat_name: str


class CreateChatResponseSchema(BaseModel):
    chat_id: str

    @classmethod
    def from_entity(cls, chat: Chat) -> 'CreateChatResponseSchema':
        return cls(chat_id=chat.id)

CredentialsUserRequestSchema = Annotated[OAuth2PasswordRequestForm, Depends()]

RegistrationUserRequestSchema = Annotated[str, Query(alias="token")]
