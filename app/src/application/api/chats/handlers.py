from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from punq import Container

from application.api.schemas import ErrorSchema, auth_user
from application.api.users.schemas import CredentialsUserRequestSchema, RegistrationUserRequestSchema
from domain.entities.access_token import AccessToken
from domain.exceptions.base import ApplicationException
from domain.values.password import Password
from logic import _init_container, Mediator
from logic.commands.users import RegistrateUserCommand, CheckExistsEmail, ValidateRegistrationCommand

router = APIRouter(tags=["Chats"])


@router.put("/create-chat",
            status_code=status.HTTP_201_CREATED,
            description="Эндпоинт для создания нового чата",
            responses={
                status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
            })
async def create_chat(access_token: AccessToken = Depends(auth_user), container: Container = Depends(_init_container)):
    container.resolve()

