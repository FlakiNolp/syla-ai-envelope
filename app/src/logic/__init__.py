import asyncio
import logging
from functools import lru_cache

from bson import UuidRepresentation
from joserfc.rfc7518.rsa_key import RSAKey
from punq import Container, Scope
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient

from configs.config import ConfigSettings
from infrastructure.email_service.base import BaseEmailService
from infrastructure.email_service.email_service import EmailService
from infrastructure.jwt.base import BaseJWT
from infrastructure.jwt.rsa import RSAJWT
from infrastructure.repositories.messages.base import BaseMessagesRepository
from infrastructure.repositories.messages.mongodb import MongoDBMessagesRepository
from infrastructure.unit_of_work.base import BaseUnitOfWork
from infrastructure.unit_of_work.mongodb import MongoDBUnitOfWork
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

    def init_logger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # Обработчик для записи логов в файл
        file_handler = logging.FileHandler(r"logic/logs/main.log")
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Обработчик для вывода логов в консоль
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # Добавляем обработчики в логгер
        if not logger.hasHandlers():
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

    container.register(logging.Logger, factory=init_logger, scope=Scope.singleton)

    container.register(ConfigSettings, instance=ConfigSettings(), scope=Scope.singleton)

    with open("logic/secrets/private_key.pem", "rb") as f:
        container.register(BaseJWT, instance=RSAJWT(key=RSAKey.import_key(value=f.read())), scope=Scope.singleton)

    container.register(BaseEmailService, EmailService, host='smtp.gmail.com', port=587, sender_email='check.telegram.bot@gmail.com', sender_password='jqsoucptkviktkeg', host_server="localhost:8000")

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

    container.register(Mediator, factory=init_mediator)

    return container
