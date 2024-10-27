import abc
import datetime
import enum
from joserfc import jwt
from joserfc.jwk import RSAKey

from domain.entities.access_token import AccessToken
from domain.entities.pair_tokens import PairTokens
from domain.entities.refresh_token import RefreshToken


class TokenType(enum.Enum):
    access_token = "access_token"
    refresh_token = "refresh_token"


class BaseJWT[T: PairTokens | AccessToken | RefreshToken, TK: RSAKey](abc.ABC):
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
