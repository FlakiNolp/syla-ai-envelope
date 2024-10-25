from typing import Annotated

from fastapi import Header
from pydantic import BaseModel, Field

from domain.entities.pair_tokens import PairTokens


class AuthenticateUserResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    @classmethod
    def from_entity(cls, pair_tokens: PairTokens) -> "AuthenticateUserResponseSchema":
        return cls(
            access_token=pair_tokens.access_token,
            refresh_token=pair_tokens.refresh_token,
            token_type="Bearer"
        )


RefreshAuthorizationUserRequestSchema = Annotated[str, Header(..., name="Authorization")]

AccessAuthorizationUserReqeustSchema = Annotated[str, Header(..., name="Authorization")]


# class RefreshAuthenticateUserResponseSchema(BaseModel):
#     access_token: str
#     token_type: str
#
#     @classmethod
#     def from_entity(cls, access_token: EncodedToken) -> "RefreshAuthenticateUserResponseSchema":
#         return cls(access_token=access_token.as_generic_type(), token_type="Bearer")
#
#
# class CreateProjectReqeustSchema(BaseModel):
#     project_oid: str = Field(..., alias="project_id")
#     scopes: list[str] = Field(...)
#
#
# class CreateProjectResponseSchema(BaseModel):
#     project_token: str
#     token_type: str
#
#     @classmethod
#     def from_entity(cls, project_token: EncodedToken) -> "CreateProjectResponseSchema":
#         return cls(project_token=project_token.model_dump(), token_type="Bearer")
