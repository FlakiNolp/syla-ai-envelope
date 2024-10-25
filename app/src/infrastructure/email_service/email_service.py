import asyncio
from dataclasses import dataclass
from typing import Any
import aiosmtplib
from email.message import EmailMessage

from domain.values.email import Email
from infrastructure.email_service.base import BaseEmailService
from infrastructure.exceptions.email_service import SendEmailException


@dataclass
class EmailService(BaseEmailService):
    host: str
    port: int
    sender_email: Email
    sender_password: str
    host_server: str

    def __post_init__(self):
        self.server = aiosmtplib.SMTP(hostname=self.host, port=self.port,
                                      username=self.sender_email.as_generic_type(), password=self.sender_password)

    async def send(self, receiver_email: Email, subject: str, body: Any):
        message = EmailMessage()
        message['From'] = self.sender_email.as_generic_type()
        message['To'] = receiver_email.as_generic_type()
        message['Subject'] = subject
        message.set_content(body)
        try:
            async with self.server:
                await self.server.ehlo()
                await self.server.send_message(message)
        except Exception as e:
            raise SendEmailException(receiver_email.as_generic_type())

    async def send_registration_mail(self, receiver_email: Email, registration_token: str):
        self.log.info(receiver_email.as_generic_type())
        await self.send(receiver_email, 'Регистрация в DataChad', f"Ссылка для регистрации\nhttp://{self.host_server}/registration?token={registration_token}")


if __name__ == '__main__':
    service = EmailService(host='smtp.gmail.com', port=587, sender_email=Email("check.telegram.bot@gmail.com"),
                           sender_password='jqsoucptkviktkeg', host_server="localhost:8000")


    async def main():
        await service.send_registration_mail(Email("maxim.osetrov-2016@yandex.ru"), registration_token="Такой токен")


    asyncio.run(main())
