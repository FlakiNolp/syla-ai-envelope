from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class ConfigSettings(BaseSettings):
    db_host: str = Field("localhost", alias="DB_HOST")  # По умолчанию ip сервера базы данных localhost
    db_port: int = Field(5432, alias="DB_PORT")  # По умолчанию порт сервера базы данных 5432
    db_username: str = Field("postgres", alias="DB_USERNAME")  # По умолчанию пользователь сервера базы данных postgres
    db_password: str = Field(
        "postgres", alias="DB_PASSWORD"
    )  # По умолчанию пароль у пользователя сервера базы данных postgres
    db_database: str = Field("envelope", alias="DB_DATABASE")  # По умолчанию название базы данных сервера envelope
