from dataclasses import dataclass

from domain.values.base import BaseValueObject
from domain.values.alg import Alg


@dataclass(frozen=True)
class JWTHeader(BaseValueObject):
    value: Alg

    def validate(self): ...

    def as_generic_type(self) -> dict:
        return {"alg": self.value.as_generic_type(), "typ": "JWT"}
