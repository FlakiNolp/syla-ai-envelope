from dataclasses import dataclass

from domain.exceptions.chat_name import ChatNameLengthException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class ChatName(BaseValueObject):
    value: str

    def validate(self):
        if 3 > len(self.value) > 255:
            raise ChatNameLengthException(self.value)

    def as_generic_type(self) -> str:
        return self.value
