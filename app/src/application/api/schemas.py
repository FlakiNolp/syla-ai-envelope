from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from punq import Container
from pydantic import BaseModel

from domain.entities.access_token import AccessToken
from domain.exceptions.base import ApplicationException
from logic import _init_container
from logic.commands.users import AuthorizeUser
from logic.mediator.base import Mediator


async def auth_user(token: Annotated[str, Header(alias="Authorization")], container: Container = Depends(_init_container)) -> AccessToken:
    try:
        mediator: Mediator = container.resolve(Mediator)
        return (await mediator.handle_command(AuthorizeUser(token.split()[-1])))[0]
    except ApplicationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"error": e.message})


class ErrorSchema(BaseModel):
    error: str
