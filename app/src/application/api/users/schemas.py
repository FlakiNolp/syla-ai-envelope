from typing import Annotated
from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordRequestForm

CredentialsUserRequestSchema = Annotated[OAuth2PasswordRequestForm, Depends()]

RegistrationUserRequestSchema = Annotated[str, Query(alias="token")]
