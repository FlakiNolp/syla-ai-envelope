from typing import Annotated
from punq import Container
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from application.api.schemas import ErrorSchema
from application.api.users.schemas import AuthenticateUserResponseSchema
from domain.exceptions.base import ApplicationException
from logic import _init_container, Mediator
from logic.commands.users import AuthenticateUserCommand

router = APIRouter(tags=['Users'])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", scopes={"read_api": "read-api", "write-api": "write-api", "post-api": "post new items"})


@router.post("/token", status_code=status.HTTP_200_OK, description="Эндпоинт верифицирует пользователя и возвращает пару токенов access-token и refresh-token",
             responses={
                 status.HTTP_200_OK: {"model": AuthenticateUserResponseSchema},
                 status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema},
             })
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], container: Container = Depends(_init_container)):
    mediator: Mediator = container.resolve(Mediator)
    try:
        pair_tokens, *_ = await mediator.handle_command(AuthenticateUserCommand(email=form_data.username, password=form_data.password))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": e.message})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": str(e)})
    return AuthenticateUserResponseSchema.from_entity(pair_tokens)


# @router.post("/refresh", status_code=status.HTTP_200_OK, description="Эндпоинт верифицирует refresh-token и возвращает access-token",
#              responses={
#                  status.HTTP_200_OK: {"model": RefreshAuthenticateUserResponseSchema},
#                  status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema}
#              })
# async def refresh(refresh_token: RefreshAuthorizationUserRequestSchema, container: Container = Depends(_init_container)):
#     mediator: Mediator = container.resolve(Mediator)
#     try:
#         access_token, *_ = await mediator.handle_command(RefreshAuthenticateUserCommand(refresh_token=refresh_token))
#     except ApplicationException as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": e.message})
#     return RefreshAuthenticateUserResponseSchema.from_entity(access_token)


# @router.post(
#     "/create-project-token",
#     status_code=status.HTTP_201_CREATED,
#     description="Эндпоинт аутентифицирует пользователя по access-token создает project-token",
#     responses={
#         status.HTTP_201_CREATED: {"model": CreateProjectToken},
#         status.HTTP_401_UNAUTHORIZED: {"model": ErrorSchema},
#     })
# async def create_project_token(access_token: AccessAuthorizationUserReqeustSchema,
#                                project_data: CreateProjectReqeustSchema,
#                                container: Container = Depends(_init_container)):
#     mediator: Mediator = container.resolve(Mediator)
#     try:
#         project_token, *_ = await mediator.handle_command(CreateProjectToken(access_token=access_token,
#                                                                              project_oid=project_data.project_oid,
#                                                                              scopes=project_data.scopes))
#     except ApplicationException as e:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": e.message})
#     return CreateProjectResponseSchema.from_entity(project_token)

