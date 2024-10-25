from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class JWTVerifyException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f"Ошибка верификации jwt токена <{self.text}>"


@dataclass(frozen=True, eq=False)
class JWTCreationException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f"Ошибка создания jwt токена <{self.text}>"


@dataclass(frozen=True, eq=False)
class JWTValidationPairException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f"Ошибка создания пары токенов <{self.text}>"


@dataclass(frozen=True, eq=False)
class JWTHeaderException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f"Ошибка создания заголовка jwt <{self.text}>"


@dataclass(frozen=True, eq=False)
class JWTPayloadException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f"Ошибка создания тела jwt <{self.text}>"


@dataclass(frozen=True, eq=False)
class JWTAlgValidationException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        return f"Ошибка валидации alg <{self.text}>"
