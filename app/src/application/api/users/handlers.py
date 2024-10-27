from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from punq import Container

from application.api.schemas import ErrorSchema, auth_user
from application.api.users.schemas import CredentialsUserRequestSchema, RegistrationUserRequestSchema
from domain.exceptions.base import ApplicationException
from domain.values.password import Password
from logic import _init_container, Mediator
from logic.commands.users import RegistrateUserCommand, CheckExistsEmail, ValidateRegistrationCommand

router = APIRouter(tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://localhost:8001/token",
    scopes={"read_api": "read-api", "write-api": "write-api", "post-api": "post new items"},
)


@router.post(
    "/sign-up",
    status_code=status.HTTP_202_ACCEPTED,
    description="Эндпоинт для регистрации пользователя и отправки письма на почту",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def sign_up(
    credentials: CredentialsUserRequestSchema, background_tasks: BackgroundTasks, container=Depends(_init_container)
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        user_exists = (await mediator.handle_command(CheckExistsEmail(credentials.username)))[0]
        if not user_exists:
            Password(credentials.password)
            background_tasks.add_task(
                mediator.handle_command, RegistrateUserCommand(credentials.username, credentials.password)
            )
            return Response(status_code=status.HTTP_202_ACCEPTED)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": "Пользователь с такой почтой уже существует"}
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message})


@router.get(
    "/registration",
    status_code=status.HTTP_201_CREATED,
    description="Ендпоинт для валидации токена с почты и создания пользователя при успешной валидации",
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema}},
)
async def registration(registration_token: RegistrationUserRequestSchema, container=Depends(_init_container)):
    try:
        mediator: Mediator = container.resolve(Mediator)
        new_user, *_ = await mediator.handle_command(ValidateRegistrationCommand(registration_token))
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message})
    return new_user
