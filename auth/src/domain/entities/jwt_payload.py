import datetime
from dataclasses import dataclass, field
from typing import TypedDict, override, Any, Iterable, Literal

from domain.exceptions.jwt import JWTPayloadException
from domain.entities.base import BaseEntity
from domain.values.base import BaseValueObject
from domain.values.id import uuid7_gen


class Sub(TypedDict, total=False):
    id: str
    type: Literal["access", "refresh", "project", "registration"]
    scopes: list[str]
    email: str
    hashed_password: str


@dataclass
class JWTPayload(BaseEntity):
    jti: str = field(default_factory=lambda: str(uuid7_gen()))
    iss: str | None = field(default=None)
    sub: Sub = field(default=None)
    iat: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(seconds=60), kw_only=True
    )
    exp: datetime.datetime | datetime.timedelta = field(default=None, kw_only=True)
    nbf: datetime.datetime | None = field(default=None)
    aud: list[str] | None = field(default=None)

    def __post_init__(self) -> None:
        if isinstance(self.iat, int):
            self.iat = datetime.datetime.fromtimestamp(self.iat)
        if isinstance(self.exp, int):
            self.exp = datetime.datetime.fromtimestamp(self.exp)
        if isinstance(self.nbf, int):
            self.nbf = datetime.datetime.fromtimestamp(self.nbf)
        if isinstance(self.exp, datetime.timedelta):
            self.exp += self.iat
        if isinstance(self.nbf, datetime.timedelta):
            self.nbf += self.iat

        self.validate()

    def validate(self):
        if self.exp is not None and self.exp <= self.iat:
            raise JWTPayloadException(
                "параметр exp должен быть больше ias"
            )
        if self.nbf is not None and self.nbf <= self.iat:
            raise JWTPayloadException(
                "параметр nbf должен быть больше ias"
            )
        if isinstance(self.aud, list):
            raise JWTPayloadException("параметр aud должен быть списком")

    @override
    def model_dump(self) -> dict:

        def to_dict_recursive(obj: Any) -> Any:
            if isinstance(obj, BaseValueObject):
                return obj.as_generic_type()
            elif isinstance(obj, BaseEntity):
                return {
                    key: to_dict_recursive(value)
                    for key, value in obj.model_dump().items()
                }
            elif isinstance(obj, dict):
                return obj
            elif isinstance(obj, Iterable) and not isinstance(obj, str):
                return [to_dict_recursive(item) for item in obj]
            elif isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
                return obj.timestamp()
            else:
                return obj

        dict_payload = {
            key: to_dict_recursive(value) for key, value in self.__dict__.items()
            if value is not None
        }
        dict_payload.pop("id")
        return dict_payload
