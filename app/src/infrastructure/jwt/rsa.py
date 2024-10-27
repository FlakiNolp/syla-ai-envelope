import datetime
from joserfc import jwt, errors
from joserfc.jwk import RSAKey, JWKRegistry
from joserfc.jwt import Token

from domain.entities.access_token import AccessToken
from domain.entities.registration_token import RegistrationToken
from domain.values.alg import Alg
from domain.entities.jwt_payload import JWTPayload
from domain.values.jwt_header import JWTHeader
from domain.exceptions.jwt import JWTVerifyException
from infrastructure.jwt.base import BaseJWT
from infrastructure.jwt.base import TokenType


class RSAJWT[T: AccessToken | RegistrationToken, TK: RSAKey](BaseJWT):
    def __init__(
        self,
        key: TK,
        registry: jwt.JWTClaimsRegistry = jwt.JWTClaimsRegistry(),
        access_token_expires_in: datetime.timedelta = datetime.timedelta(days=1),
        refresh_token_expires_in: datetime.timedelta = datetime.timedelta(days=30),
        registration_token_expires_in: datetime.timedelta = datetime.timedelta(minutes=15),
    ):
        self.key = key
        self.registry = registry
        self.access_token_expires_in = access_token_expires_in
        self.refresh_token_expires_in = refresh_token_expires_in
        self.registration_token_expires_in = registration_token_expires_in

    def encode(self, token: T) -> str | tuple[str, str]:
        if isinstance(token, AccessToken):
            token.payload.exp = token.payload.iat + self.access_token_expires_in
            return jwt.encode(
                header=token.header.as_generic_type(),
                claims=token.payload.model_dump(),
                key=self.key,
                algorithms=[token.header.value.as_generic_type()],
            )
        elif isinstance(token, RegistrationToken):
            if self.registration_token_expires_in:
                token.payload.exp = token.payload.iat + self.registration_token_expires_in
            return jwt.encode(
                header=token.header.as_generic_type(),
                claims=token.payload.model_dump(),
                key=self.key,
                algorithms=[token.header.value.as_generic_type()],
            )

    @staticmethod
    def convert_from_token_to_entity(token: Token, _type: TokenType) -> T:
        match _type:
            case TokenType.access_token:
                return AccessToken(header=JWTHeader(value=Alg(token.header["alg"])), payload=JWTPayload(**token.claims))
            case TokenType.registration_token:
                return RegistrationToken(
                    header=JWTHeader(value=Alg(token.header["alg"])), payload=JWTPayload(**token.claims)
                )

    def _decode(self, token: str) -> jwt.Token:
        try:
            print(token)
            return jwt.decode(value=token, key=self.key)
        except errors.JoseError as e:
            raise JWTVerifyException(text=token)

    def decode(self, token: str, _type: TokenType) -> T:
        decoded_token = self._decode(token)
        if decoded_token:
            return self.convert_from_token_to_entity(decoded_token, _type)

    def verify(self, token: str, _type: TokenType) -> T | None:
        if isinstance(token, str):
            self.validate(token)
            decoded_token = self._decode(token)
            return self.convert_from_token_to_entity(decoded_token, _type)

    def validate(self, token: str | jwt.Token) -> None:
        try:
            if isinstance(token, str):
                decoded_token = self._decode(token)
                self.registry.validate(decoded_token.claims)
            elif isinstance(token, jwt.Token):
                self.registry.validate(token.claims)
        except errors.JoseError as e:
            raise JWTVerifyException(text=token)
