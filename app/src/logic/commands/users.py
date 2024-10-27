from dataclasses import dataclass

from infrastructure.unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork
from domain.entities.access_token import AccessToken
from domain.entities.jwt_payload import JWTPayload
from domain.entities.registration_token import RegistrationToken
from domain.entities.user import User
from domain.values.alg import Alg
from domain.values.email import Email
from domain.values.jwt_header import JWTHeader
from domain.values.password import Password, HashedPassword
from infrastructure.email_service.base import BaseEmailService
from infrastructure.jwt.base import BaseJWT, TokenType
from infrastructure.unit_of_work.base import BaseUnitOfWork
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class AuthorizeUser(BaseCommand):
    token: str


@dataclass(frozen=True)
class AuthorizeUserHandler(CommandHandler[AuthorizeUser, AccessToken]):
    jwt_service: BaseJWT

    async def handle(self, command: AuthorizeUser) -> AccessToken:
        return self.jwt_service.verify(command.token, _type=TokenType.access_token)


@dataclass(frozen=True)
class CheckExistsEmail(BaseCommand):
    email: str


@dataclass(frozen=True)
class CheckExistsEmailHandler(CommandHandler[CheckExistsEmail, bool]):
    uow: BaseUnitOfWork

    @SQLAlchemyUnitOfWork.provide_async_uow
    async def handle(self, command: CheckExistsEmail) -> bool:
        if await self.uow.users.get_by_email(Email(command.email)) is None:
            return False
        return True


@dataclass(frozen=True)
class RegistrateUserCommand(BaseCommand):
    email: str
    password: str


@dataclass(frozen=True)
class RegistrateUserCommandHandler(CommandHandler[RegistrateUserCommand, None]):
    email_service: BaseEmailService
    jwt_service: BaseJWT

    async def handle(self, command: RegistrateUserCommand):
        token = self.jwt_service.encode(
            RegistrationToken(
                JWTHeader(Alg("RS256")),
                JWTPayload(
                    sub={
                        "email": command.email,
                        "hashed_password": Password(command.password).hash_password().as_generic_type(),
                        "type": TokenType.registration_token.value
                    }
                ),
            )
        )
        await self.email_service.send_registration_mail(receiver_email=Email(command.email), registration_token=token)


@dataclass(frozen=True)
class ValidateRegistrationCommand(BaseCommand):
    token: str


@dataclass(frozen=True)
class ValidateRegistrationCommandHandler(CommandHandler[ValidateRegistrationCommand, User]):
    jwt_service: BaseJWT
    uow: BaseUnitOfWork

    @SQLAlchemyUnitOfWork.provide_async_uow
    async def handle(self, command: ValidateRegistrationCommand) -> User:
        registration_token: RegistrationToken = self.jwt_service.verify(
            token=command.token, _type=TokenType.registration_token
        )
        new_user = User.create_user(
            Email(registration_token.payload.sub["email"]),
            HashedPassword(registration_token.payload.sub["hashed_password"]),
        )
        await self.uow.users.add(new_user)
        await self.uow.commit()
        return new_user
