import abc
import datetime
import enum
from dataclasses import dataclass, field
from joserfc import jwt
from joserfc.jwk import RSAKey

from domain.entities.access_token import AccessToken
from domain.entities.refresh_token import RefreshToken



class TokenType(enum.Enum):
    access_token = 'access_token'
    refresh_token = 'refresh_token'


@dataclass
class BaseJWT[T: AccessToken | RefreshToken,TK: RSAKey](abc.ABC):
    key: TK
    registry: jwt.JWTClaimsRegistry = field(default_factory=jwt.JWTClaimsRegistry)
    access_token_expires_in: datetime.timedelta = field(default=datetime.timedelta(days=1))
    refresh_token_expires_in: datetime.timedelta = field(default=datetime.timedelta(days=30))

    @abc.abstractmethod
    def encode(self, token: T) -> str | tuple[str, str]: ...

    @abc.abstractmethod
    def _decode(self, token: str) -> jwt.Token | None: ...

    @abc.abstractmethod
    def decode(self, token: str, _type: TokenType) -> T | None: ...

    @abc.abstractmethod
    def verify(self, token: str, _type: TokenType) -> T: ...

    @abc.abstractmethod
    def validate(self, token: T) -> bool: ...
