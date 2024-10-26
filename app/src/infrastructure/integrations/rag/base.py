from dataclasses import dataclass
from abc import ABC, abstractmethod

from domain.entities.message import Message


@dataclass
class BaseRag(ABC):
    host: str
    port: int

    @abstractmethod
    async def generate_message(self, message: str) -> Message: ...
