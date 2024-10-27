from typing import Annotated

from fastapi import Header, Body
from pydantic import BaseModel

from domain.entities.pair_tokens import PairTokens


class AuthenticateUserResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    @classmethod
    def from_entity(cls, pair_tokens: PairTokens) -> "AuthenticateUserResponseSchema":
        return cls(access_token=pair_tokens.access_token, refresh_token=pair_tokens.refresh_token, token_type="Bearer")


RefreshAuthorizationUserRequestSchema = Annotated[str, Body(..., name="refresh_token")]

AccessAuthorizationUserReqeustSchema = Annotated[str, Header(..., name="Authorization")]


class RefreshAuthenticateUserResponseSchema(BaseModel):
    access_token: str
    token_type: str

    @classmethod
    def from_entity(cls, access_token: str) -> "RefreshAuthenticateUserResponseSchema":
        return cls(access_token=access_token, token_type="Bearer")
