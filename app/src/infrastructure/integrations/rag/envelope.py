from dataclasses import dataclass
from aiohttp import ClientSession
import requests

from domain.entities.message import Message
from domain.values.author import Author
from domain.values.id import UUID7
from infrastructure.integrations.rag.base import BaseRag


@dataclass
class Rag(BaseRag):
    host: str
    port: int

    async def generate_answer(self, message: Message, chat_id: UUID7) -> Message:
        async with ClientSession() as client:
            async with client.post(f"http://{self.host}:{self.port}/qa/answer", json={"query": message.text}, ssl=False) as response:
                if not response.ok:
                    raise
                response_json = await response.json()
                return Message(chat_id=chat_id, text=response_json['answer'], documents=response_json['pics'], author=Author.ai)
