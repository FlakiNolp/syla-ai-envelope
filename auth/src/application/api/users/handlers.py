import datetime
import json
from typing import Annotated
from punq import Container
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from domain.entities.pair_tokens import PairTokens
from application.api.schemas import ErrorSchema
from application.api.users.schemas import AuthenticateUserResponseSchema, RefreshAuthenticateUserResponseSchema, \
    RefreshAuthorizationUserRequestSchema
from domain.exceptions.base import ApplicationException
from logic import _init_container, Mediator
from logic.commands.users import AuthenticateUserCommand, RefreshAuthenticateUserCommand

router = APIRouter(tags=['Users'])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", scopes={"read_api": "read-api", "write-api": "write-api", "post-api": "post new items"})


@router.post("/token", status_code=status.HTTP_200_OK, description="Эндпоинт верифицирует пользователя и возвращает пару токенов access-token и refresh-token",
             responses={
                 status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema},
             })
async def token(response: JSONResponse, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], container: Container = Depends(_init_container)):
    try:
        mediator: Mediator = container.resolve(Mediator)
        pair_tokens: PairTokens = (await mediator.handle_command(AuthenticateUserCommand(email=form_data.username, password=form_data.password)))[0]
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": e.message})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": str(e)})
    response.status_code = 200
    response.body = AuthenticateUserResponseSchema.from_entity(pair_tokens).model_dump_json().encode()
    response.set_cookie(key="refresh_token", value=pair_tokens.refresh_token,
                        expires=int(datetime.timedelta(days=30).total_seconds()), httponly=True, samesite=None, domain="31.129.50.189:8001")
    return response


@router.post("/refresh", status_code=status.HTTP_200_OK, description="Эндпоинт верифицирует refresh-token и возвращает access-token",
             responses={
                 status.HTTP_200_OK: {"model": RefreshAuthenticateUserResponseSchema},
                 status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema}
             })
async def refresh(refresh_token: RefreshAuthorizationUserRequestSchema, container: Container = Depends(_init_container)):
    try:
        mediator: Mediator = container.resolve(Mediator)
        access_token, *_ = await mediator.handle_command(RefreshAuthenticateUserCommand(refresh_token=refresh_token))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": e.message})
    except Exception as e:
        raise e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": str(e)})
    return RefreshAuthenticateUserResponseSchema.from_entity(access_token)
