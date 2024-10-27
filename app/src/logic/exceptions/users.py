from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class UserEmailExistsException(LogicException):
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
class UserIdExistsException(LogicException):
    text: str

    @property
    def message(self):
        return f"Пользователя с id <{self.text}> не сущесвует"
