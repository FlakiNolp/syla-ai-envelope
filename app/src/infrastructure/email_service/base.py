import abc
import logging
from dataclasses import dataclass
from typing import Any

from domain.values.email import Email


@dataclass
class BaseEmailService(abc.ABC):
    @abc.abstractmethod
    async def send(self, receiver_email: Email, subject: str, body: Any): ...
    @abc.abstractmethod
    async def send_registration_mail(self, receiver_email: Email, registration_token: str) -> None: ...
