import datetime
from aiohttp import ClientSession, ClientResponse

from domain.entities.message import Message
from domain.values.author import Author
from domain.values.id import UUID7
from infrastructure.exceptions.rag import RagRequestException
from infrastructure.integrations.rag.base import BaseRag


class Rag(BaseRag):
    def __init__(self, host: str, port: int, retry_attempts: int = 3, timeout: int = 20):
        self.host: str = host
        self.port: int = port
        self.retry_attempts: int = retry_attempts
        self.timeout: int = timeout

    async def send_requests_with_repeat(self, client: ClientSession, message: Message) -> dict:
        async with client.post(
            f"http://{self.host}:{self.port}/qa/answer", json={"query": message.text, "tok_k": 2, "top_k_img": 5}, timeout=self.timeout
        ) as response:
            print(response.status)
            if not response.ok:
                return None
            return await response.json()

    async def generate_answer(self, message: Message, chat_id: UUID7) -> Message | None:
            async with ClientSession() as client:
                response_json = await self.send_requests_with_repeat(client, message)
                if response_json is None:
                    return None
                return Message(
                    chat_id=chat_id, text=response_json["answer"], documents=response_json["pics"], author=Author.ai
                )
