from dataclasses import dataclass
from abc import ABC, abstractmethod

from domain.entities.message import Message
from domain.values.id import UUID7


class BaseRag(ABC):
    @abstractmethod
    async def generate_answer(self, message: Message, chat_id: UUID7) -> Message | None: raise NotImplementedError
