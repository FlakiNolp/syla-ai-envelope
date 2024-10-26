from dataclasses import dataclass
import datetime

from domain.entities.base import BaseEntity
from domain.entities.jwt_payload import JWTPayload
from domain.values.alg import Alg
from domain.values.jwt_header import JWTHeader


@dataclass
class RegistrationToken(BaseEntity):
    header: JWTHeader
    payload: JWTPayload

    def as_generic_type(self):
        return {"header": self.header.as_generic_type(), "payload": self.payload.model_dump()}

    @property
    def sub(self):
        return self.payload.sub
