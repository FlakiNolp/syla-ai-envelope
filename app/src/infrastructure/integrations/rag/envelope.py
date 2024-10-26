from dataclasses import dataclass
from abc import ABC, abstractmethod
from aiohttp import ClientSession

from domain.entities.message import Message
from domain.values.author import Author
from domain.values.id import UUID7


@dataclass
class Rag(ABC):
    host: str
    port: int

    async def generate_message(self, message: Message, chat_id: UUID7) -> Message:
        async with ClientSession() as client:
            async with client.post(f"http://{self.host}:{self.port}/generate", json={"text": message.text}) as response:
                if not response.ok:
                    raise
                res = await response.json()
                return Message(chat_id=chat_id, text=res['text'], documents=res['documents'], author=Author.ai)
