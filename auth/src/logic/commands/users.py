from dataclasses import dataclass
import hashlib

from domain.values.email import Email
from domain.values.id import UUID7
from infrastructure.jwt.base import BaseJWT, TokenType
from infrastructure.repositories.users.base import BaseUserRepository
from infrastructure.unit_of_work.base import BaseUnitOfWork
from infrastructure.unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork
from logic.commands.base import BaseCommand, CommandHandler
from domain.entities.pair_tokens import PairTokens
from domain.entities.access_token import AccessToken

# from domain.entities.encoded_token import EncodedToken
from domain.entities.refresh_token import RefreshToken
from logic.exceptions.users import UserAuthenticateException, RefreshAuthenticateException
from domain.values.jwt_header import JWTHeader
from domain.values.alg import Alg
from domain.entities.jwt_payload import JWTPayload, Sub


@dataclass(frozen=True)
class AuthenticateUserCommand(BaseCommand):
    email: str
    password: str


@dataclass(frozen=True)
class AuthenticateUserCommandHandler(CommandHandler[AuthenticateUserCommand, PairTokens]):
    uow: BaseUnitOfWork
    jwt_factory: BaseJWT

    @SQLAlchemyUnitOfWork.provide_async_uow
    async def handle(self, command: AuthenticateUserCommand) -> PairTokens:
        user = await self.uow.users.get_by_email(Email(command.email))
        if user is None or user.password.as_generic_type() != hashlib.sha256(command.password.encode()).hexdigest():
            raise UserAuthenticateException()
        access_token = self.jwt_factory.encode(
            AccessToken(
                header=JWTHeader(value=Alg("RS256")), payload=JWTPayload(sub=Sub(id=str(user.id), type="access"))
            )
        )
        refresh_token = self.jwt_factory.encode(
            RefreshToken(
                header=JWTHeader(value=Alg("RS256")), payload=JWTPayload(sub=Sub(id=str(user.id), type="refresh"))
            )
        )
        return PairTokens(access_token=access_token, refresh_token=refresh_token)


@dataclass(frozen=True)
class RefreshAuthenticateUserCommand(BaseCommand):
    refresh_token: str


@dataclass(frozen=True)
class RefreshAuthenticateUserCommandHandler(CommandHandler[RefreshAuthenticateUserCommand, str]):
    uow: BaseUnitOfWork
    jwt_factory: BaseJWT

    @SQLAlchemyUnitOfWork.provide_async_uow
    async def handle(self, command: RefreshAuthenticateUserCommand) -> str:
        refresh_token: RefreshToken = self.jwt_factory.verify(
            token=command.refresh_token, _type=TokenType.refresh_token
        )
        if await self.uow.users.get_by_id(UUID7(refresh_token.sub_id)):
            return self.jwt_factory.encode(
                AccessToken(
                    header=JWTHeader(value=Alg("RS256")),
                    payload=JWTPayload(sub=Sub(id=refresh_token.sub_id, type="access")),
                )
            )
        raise RefreshAuthenticateException(refresh_token.sub_id)
