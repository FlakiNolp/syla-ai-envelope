from typing import Any
import aiosmtplib
from email.message import EmailMessage

from domain.values.email import Email
from infrastructure.email_service.base import BaseEmailService
from infrastructure.exceptions.email_service import SendEmailException


class EmailService(BaseEmailService):
    def __init__(self, host: str, port: int, sender_email: str, sender_password: str, host_server: str):
        self.host = host
        self.port = port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.host_server = host_server
        self.server = aiosmtplib.SMTP(
            hostname=self.host, port=self.port, username=self.sender_email, password=self.sender_password
        )

    async def send(self, receiver_email: Email, subject: str, body: Any):
        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = receiver_email.as_generic_type()
        message["Subject"] = subject
        message.set_content(body)
        try:
            async with self.server:
                await self.server.ehlo()
                await self.server.send_message(message)
        except Exception as e:
            raise SendEmailException(receiver_email.as_generic_type())

    async def send_registration_mail(self, receiver_email: Email, registration_token: str):
        await self.send(
            receiver_email,
            "Регистрация",
            f"Ссылка для регистрации\nhttp://{self.host_server}/registration?token={registration_token}",
        )
