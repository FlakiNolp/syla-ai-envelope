import datetime
from aiohttp import ClientSession, ClientResponse

from domain.entities.message import Message
from domain.values.author import Author
from domain.values.id import UUID7
from infrastructure.exceptions.rag import RagRequestException
from infrastructure.integrations.rag.base import BaseRag


class Rag(BaseRag):
    def __init__(self, host: str, port: int, retry_attempts: int = 3, timeout: int = 15):
        self.host: str = host
        self.port: int = port
        self.retry_attempts: int = retry_attempts
        self.timeout: int = timeout

    async def send_requests_with_repeat(self, client: ClientSession, message: Message) -> dict:
        async with client.post(
            f"http://{self.host}:{self.port}/qa/answer", json={"query": message.text}, timeout=self.timeout
        ) as response:
            if not response.ok:
                raise response.raise_for_status()
            return await response.json()

    async def generate_answer(self, message: Message, chat_id: UUID7) -> Message | None:
        try:
            async with ClientSession() as client:
                i = 0
                while i < self.retry_attempts:
                        i += 1
                        response_json = await self.send_requests_with_repeat(client, message)
                        return Message(
                            chat_id=chat_id, text=response_json["answer"], documents=response_json["pics"], author=Author.ai
                        )
                return None
        except Exception as e:
            return None
