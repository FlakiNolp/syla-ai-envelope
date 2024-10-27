from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from punq import Container

from application.api.messages.schemas import (
    ReceivedMessageRequestSchema,
    JSONMessage,
    GetHistoryRequestSchema,
    GetHistoryResponseSchema,
)
from application.api.schemas import ErrorSchema, auth_user
from domain.entities.access_token import AccessToken
from domain.entities.message import Message
from domain.exceptions.base import ApplicationException
from logic import _init_container, Mediator
from logic.commands.message import ReceivedMessage
from logic.queries.message import GetHistoryMessages

router = APIRouter(tags=["Messages"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://localhost:8001/token",
    scopes={"read_api": "read-api", "write-api": "write-api", "post-api": "post new items"},
)


@router.post(
    "/message",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт Q&A",
    responses={
        status.HTTP_200_OK: {"model": JSONMessage},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def post_message(
    data: ReceivedMessageRequestSchema,
    access_token: AccessToken = Depends(auth_user),
    container=Depends(_init_container),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        message: Message = (
            await mediator.handle_command(
                ReceivedMessage(data.message, chat_id=data.chat_id, user_id=access_token.sub_id)
            )
        )[0]
    except ApplicationException as e:
        raise e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message})
    return JSONMessage.from_entity(message)


@router.get(
    "/message",
    status_code=status.HTTP_200_OK,
    description="Эндпоинт для получения истории чата",
    responses={
        status.HTTP_200_OK: {"model": GetHistoryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_message(
    data: GetHistoryRequestSchema = Depends(),
    access_token: AccessToken = Depends(auth_user),
    container=Depends(_init_container),
):
    try:
        mediator: Mediator = container.resolve(Mediator)
        messages: list[Message] = await mediator.handle_query(
            GetHistoryMessages(user_id=access_token.sub_id, chat_id=data.chat_id)
        )
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"error": e.message})
    return GetHistoryResponseSchema.from_entity(messages)
