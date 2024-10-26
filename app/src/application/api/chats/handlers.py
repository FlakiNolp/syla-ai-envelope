from fastapi import APIRouter, Depends, status
from punq import Container

from application.api.chats.schemas import GetChatsResponseSchema, CreateChatResponseSchema, CreateChatRequestSchema
from application.api.schemas import ErrorSchema, auth_user
from domain.entities.access_token import AccessToken
from domain.entities.chat import Chat
from domain.exceptions.base import ApplicationException
from logic import _init_container, Mediator
from logic.commands.chats import CreateChat
from logic.queries.chats import GetChats

router = APIRouter(tags=["Chats"])


@router.put("/create-chat",
            status_code=status.HTTP_201_CREATED,
            description="Эндпоинт для создания нового чата",
            responses={
                status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
                status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
            })
async def create_chat(data: CreateChatRequestSchema,  access_token: AccessToken = Depends(auth_user), container: Container = Depends(_init_container)):
    try:
        mediator: Mediator = container.resolve(Mediator)
        chat: Chat = (await mediator.handle_command(CreateChat(access_token.sub_id, data.chat_name)))[0]
    except ApplicationException as e:
        raise e
    return CreateChatResponseSchema.from_entity(chat)


@router.get("/chats",
            status_code=status.HTTP_200_OK,
            description="Эндпоинт для получения всех чатов пользователя",
            responses={
                status.HTTP_200_OK: {"model": GetChatsResponseSchema},
                status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
            })
async def get_chats(access_token: AccessToken = Depends(auth_user), container: Container = Depends(_init_container)):
    try:
        mediator: Mediator = container.resolve(Mediator)
        chats = await mediator.handle_query(GetChats(access_token.sub_id))
    except ApplicationException as e:
        raise e
    return GetChatsResponseSchema.from_entity(chats)
