from dataclasses import dataclass
import re

from domain.entities.base import BaseEntity
from domain.entities.access_token import AccessToken
from domain.entities.refresh_token import RefreshToken
from domain.exceptions.jwt import JWTValidationPairException


@dataclass
class PairTokens(BaseEntity):
    access_token: AccessToken | str
    refresh_token: RefreshToken | str

    def __post_init__(self):
        if isinstance(self.access_token, str) and isinstance(self.refresh_token, str):
            if not re.match(r"^(?:[\w-]*\.){2}[\w-]*$", self.access_token):
                raise JWTValidationPairException(self.access_token)
            if not re.match(r"^(?:[\w-]*\.){2}[\w-]*$", self.refresh_token):
                raise JWTValidationPairException(self.refresh_token)
        elif not (
            isinstance(self.access_token, AccessToken)
            and isinstance(self.refresh_token, RefreshToken)
        ):
            raise JWTValidationPairException(self.access_token)
