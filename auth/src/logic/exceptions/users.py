from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class EmailExistsException(LogicException):
    text: str

    @property
    def message(self):
        return f"Пользователь с почтой <{self.text}> уже существует"


@dataclass(frozen=True, eq=False)
class UserAuthenticateException(LogicException):
    @property
    def message(self):
        return f"Неверная почта или пароль"


@dataclass(frozen=True, eq=False)
class RefreshAuthenticateException(LogicException):
    text: str

    @property
    def message(self):
        return f"Пользователя с oid <{self.text}> не найден"
