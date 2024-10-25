from dataclasses import dataclass

from infrastructure.exceptions.base import InfrastructureException


@dataclass(frozen=True, eq=False)
class SendEmailException(InfrastructureException):
    text: str

    @property
    def message(self) -> str:
        return f"Не удалось отправить сообщение на почтовый адрес <{self.text}>"
