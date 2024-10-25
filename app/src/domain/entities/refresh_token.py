from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.values.jwt_header import JWTHeader
from domain.entities.jwt_payload import JWTPayload


@dataclass
class RefreshToken(BaseEntity):
    header: JWTHeader
    payload: JWTPayload

    def as_generic_type(self):
        return {"header": self.header, "payload": self.payload.model_dump()}
