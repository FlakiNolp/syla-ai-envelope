import logging
from functools import lru_cache

from joserfc.rfc7518.rsa_key import RSAKey
from punq import Container, Scope
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient

from configs.config import ConfigSettings
from infrastructure.email_service.base import BaseEmailService
from infrastructure.email_service.email_service import EmailService
from infrastructure.integrations.rag.base import BaseRag
from infrastructure.integrations.rag.envelope import Rag
from infrastructure.jwt.base import BaseJWT
from infrastructure.jwt.rsa import RSAJWT
from infrastructure.repositories.messages.base import BaseMessagesRepository
from infrastructure.repositories.messages.mongodb import MongoDBMessagesRepository
from infrastructure.unit_of_work.base import BaseUnitOfWork
from infrastructure.unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork
from logic.commands.chats import CreateChatHandler, CreateChat
from logic.commands.message import ReceivedMessage, ReceivedMessageHandler
from logic.commands.users import AuthorizeUser, AuthorizeUserHandler, CheckExistsEmailHandler, \
    RegistrateUserCommandHandler, ValidateRegistrationCommandHandler, CheckExistsEmail, RegistrateUserCommand, \
    ValidateRegistrationCommand
from logic.mediator.base import Mediator
from logic.queries.chats import GetChatsHandler, GetChats
from logic.queries.message import GetHistoryMessages, GetHistoryMessagesHandler


@lru_cache(1)
def _init_container():
    return init_container()


@lru_cache(None)
def init_container():
    container = Container()

    container.register(ConfigSettings, instance=ConfigSettings(), scope=Scope.singleton)

    with open("/etc/ssl/public_key.pem", "rb") as f:
        container.register(BaseJWT, instance=RSAJWT(key=RSAKey.import_key(value=f.read())), scope=Scope.singleton)

    config: ConfigSettings = container.resolve(ConfigSettings)
    container.register(BaseEmailService, EmailService, host=config.email_host, port=config.email_port, sender_email=config.email, sender_password=config.email_password, host_server=config.host_server)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # Users
        # Registrations
        container.register(CheckExistsEmailHandler)
        container.register(RegistrateUserCommandHandler)
        container.register(ValidateRegistrationCommandHandler)

        mediator.register_command(
            CheckExistsEmail, [container.resolve(CheckExistsEmailHandler)]
        )
        mediator.register_command(
            RegistrateUserCommand, [container.resolve(RegistrateUserCommandHandler)]
        )
        mediator.register_command(
            ValidateRegistrationCommand, [container.resolve(ValidateRegistrationCommandHandler)]
        )
        # Authorization
        container.register(AuthorizeUserHandler)

        mediator.register_command(
            AuthorizeUser, [container.resolve(AuthorizeUserHandler)]
        )

        # Chats
        container.register(CreateChatHandler)
        container.register(GetChatsHandler)

        mediator.register_command(CreateChat, [container.resolve(CreateChatHandler)])
        mediator.register_query(GetChats, container.resolve(GetChatsHandler))

        # Messages
        container.register(ReceivedMessageHandler)
        container.register(GetHistoryMessagesHandler)

        mediator.register_command(ReceivedMessage, [container.resolve(ReceivedMessageHandler)])
        mediator.register_query(GetHistoryMessages, container.resolve(GetHistoryMessagesHandler))

        return mediator

    def init_sqlalchemy_unit_of_work():
        config: ConfigSettings = container.resolve(ConfigSettings)
        _async_engine: AsyncEngine = create_async_engine(
            URL.create(
                drivername="postgresql+asyncpg",
                host=config.db_host,
                port=config.db_port,
                username=config.db_username,
                password=config.db_password,
                database=config.db_database,
            ),
            echo=True
        )
        _async_session_maker = async_sessionmaker(
            _async_engine, expire_on_commit=False
        )
        return SQLAlchemyUnitOfWork(_async_session_maker)

    container.register(
        BaseUnitOfWork,
        factory=init_sqlalchemy_unit_of_work,
        scope=Scope.singleton,
    )

    def init_mongodb():
        config: ConfigSettings = container.resolve(ConfigSettings)
        async_client: AsyncIOMotorClient = AsyncIOMotorClient(f"mongodb://{config.mongodb_host}:{config.mongodb_port}", uuidRepresentation="standard")
        return MongoDBMessagesRepository(mongodb_client=async_client, db_name="envelope")

    container.register(BaseMessagesRepository, factory=init_mongodb, scope=Scope.singleton)

    def init_rag_integration():
        config: ConfigSettings = container.resolve(ConfigSettings)
        return Rag(host=config.rag_host, port=config.rag_port)

    container.register(BaseRag, factory=init_rag_integration, scope=Scope.singleton)

    container.register(Mediator, factory=init_mediator)

    return container
