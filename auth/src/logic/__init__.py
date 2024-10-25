import logging
from functools import lru_cache

from joserfc.rfc7518.rsa_key import RSAKey
from punq import Container, Scope
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker

from configs.config import ConfigSettings
from infrastructure.jwt.base import BaseJWT
from infrastructure.jwt.rsa import RSAJWT
from infrastructure.unit_of_work.base import BaseUnitOfWork
from infrastructure.unit_of_work.sqlalchemy import SQLAlchemyUnitOfWork
from logic.commands.users import AuthenticateUserCommand, AuthenticateUserCommandHandler
from logic.mediator.base import Mediator
from logic.mediator.command import CommandMediator


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
    # with open(r"secrets/private_key.pem", "rb") as f:
    #     container.register(BaseJWT, instance=RSAJWT(key=RSAKey.import_key(value=container.resolve(ConfigSettings).secret_key)), scope=Scope.singleton)
    with open(r"C:\Users\maksi\PycharmProjects\syla-ai-envelope\auth\src\logic\secrets\private_key.pem", "rb") as f:
        container.register(BaseJWT, instance=RSAJWT(key=RSAKey.import_key(value=f.read())), scope=Scope.singleton)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # Users
        container.register(AuthenticateUserCommandHandler)

        mediator.register_command(AuthenticateUserCommand, [container.resolve(AuthenticateUserCommandHandler)])

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

    container.register(Mediator, factory=init_mediator)

    return container
