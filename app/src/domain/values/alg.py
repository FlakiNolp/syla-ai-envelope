from dataclasses import dataclass
from typing import Literal

from domain.exceptions.jwt import JWTHeaderException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Alg(BaseValueObject):
    value: Literal["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]

    def validate(self):
        if self.value not in ("HS256", "HS384", "HS512", "RS256", "RS384", "RS512"):
            raise JWTHeaderException("Отсутствует параметр alg")

    def as_generic_type(self) -> str:
        return self.value
