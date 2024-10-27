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
from logic.commands.users import AuthenticateUserCommand, AuthenticateUserCommandHandler, RefreshAuthenticateUserCommand, RefreshAuthenticateUserCommandHandler
from logic.mediator.base import Mediator


@lru_cache(1)
def _init_container():
    return init_container()


@lru_cache(None)
def init_container():
    container = Container()

    container.register(ConfigSettings, instance=ConfigSettings(), scope=Scope.singleton)

    with open("/etc/ssl/private_key.pem", "rb") as f:
        container.register(BaseJWT, instance=RSAJWT(key=RSAKey.import_key(value=f.read())), scope=Scope.singleton)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # Users
        container.register(AuthenticateUserCommandHandler)
        container.register(RefreshAuthenticateUserCommandHandler)

        mediator.register_command(AuthenticateUserCommand, [container.resolve(AuthenticateUserCommandHandler)])
        mediator.register_command(RefreshAuthenticateUserCommand, [container.resolve(RefreshAuthenticateUserCommandHandler)])

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
