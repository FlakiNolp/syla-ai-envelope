from dataclasses import dataclass
from joserfc import jwt, errors
from joserfc.jwk import RSAKey, JWKRegistry

from joserfc.jwt import Token

from domain.entities.access_token import AccessToken
from domain.entities.refresh_token import RefreshToken
from domain.values.alg import Alg
from domain.entities.jwt_payload import JWTPayload
from domain.values.jwt_header import JWTHeader
from domain.exceptions.jwt import JWTVerifyException
from infrastructure.exceptions.jwt import JWTEncodeException
from infrastructure.jwt.base import BaseJWT
from infrastructure.jwt.base import TokenType


@dataclass
class RSAJWT[T: AccessToken | RefreshToken](BaseJWT):
    key: RSAKey

    def encode(self, token: T) -> str | tuple[str, str]:
        try:
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
                    algorithms=[token.header.value.as_generic_type()]
                )
        except Exception as e:
            raise JWTEncodeException(str(token.id))

    @staticmethod
    def convert_from_token_to_entity(token: Token, _type: TokenType) -> T:
        match _type:
            case TokenType.access_token:
                return AccessToken(header=JWTHeader(value=Alg(token.header['alg'])), payload=JWTPayload(**token.claims))
            case TokenType.registration_token:
                return RegistrationToken(header=JWTHeader(value=Alg(token.header['alg'])), payload=JWTPayload(**token.claims))

    def _decode(self, token: str) -> jwt.Token:
        try:
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


if __name__ == "__main__":
    key = JWKRegistry.generate_key("RSA", 512)
    # print(key.private_key)
    # print(key.public_key)
    # print(key.as_pem())
    jwt2 = RSAJWT(key=key)
    with open('../../logic/secrets/private_key.pem', 'wb+') as f:
        print(key.as_pem())
        f.write(key.as_pem())
    # print(
    #     jwt2.encode(AccessToken(header=JWTHeader(Alg("RS256")), payload=JWTPayload()))
    # )
    res2 = RegistrationToken(header=JWTHeader(Alg("RS256")), payload=JWTPayload(sub={"type": "registration"}))
    res = jwt2.encode(
            res2
        )
    print(res)
    # print(
    #     jwt2.encode(
    #         ProjectToken(header=JWTHeader(Alg("RS256")), payload=JWTPayload())
    #     )
    # )
    # print(
    #     jwt2.encode(
    #         PairTokens(
    #             AccessToken(header=JWTHeader(Alg("RS256")), payload=JWTPayload()),
    #             RefreshToken(header=JWTHeader(Alg("RS256")), payload=JWTPayload()),
    #         )
    #     )
    # )
    print(jwt2._decode(res).claims)
    print(jwt2.decode(token=res, _type=TokenType.registration_token))
    print(jwt2.verify(res, _type=TokenType.registration_token))

