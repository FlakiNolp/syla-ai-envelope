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
    """
    Базовый класс для работы с JWT
    """
    @abc.abstractmethod
    def encode(self, token: T) -> str | tuple[str, str]:
        """
        Метод для создания JWT токена из сущностей
        :param token: Сущности
        :return:
        """

    @abc.abstractmethod
    def _decode(self, token: str) -> jwt.Token | None:
        """
        Метод для первичного декодирования строки JWT в JWT.Token
        :param token: Строка JWT
        :return:
        """

    @abc.abstractmethod
    def decode(self, token: str, _type: TokenType) -> T | None:
        """
        Метод для декодирования из строки JWT в сущности
        :param token: Строка JWT
        :param _type: Тип токена
        :return:
        """

    @abc.abstractmethod
    def verify(self, token: str, _type: TokenType) -> T:
        """
        Метод для валидации токена и декодирования его из строки JWT в сущности
        :param token: Строка JWT
        :param _type: Тип токена
        :return:
        """

    @abc.abstractmethod
    def validate(self, token: T) -> bool:
        """
        Метод для валидации JWT токена
        :param token: Сущности
        :return:
        """
