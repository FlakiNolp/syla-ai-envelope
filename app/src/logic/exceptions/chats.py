from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class ChatNotExistsException(LogicException):
    text: str

    @property
    def message(self):
        return f"Чата с id <{self.text}> не существует"
