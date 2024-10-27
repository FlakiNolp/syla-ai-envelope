from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(frozen=True, eq=False)
class ChatNameLengthException(ApplicationException):
    text: str

    @property
    def message(self) -> str:
        if len(self.text) > 255:
            return f"Название проекта должно быть короче 255 символов <{self.text[255:]}>"
        return f"Название проекта должно быть длинной минимум 3 символа <{self.text}>"
