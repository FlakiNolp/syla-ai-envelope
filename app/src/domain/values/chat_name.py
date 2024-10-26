from dataclasses import dataclass

from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class ChatName(BaseValueObject):
    value: str

    def validate(self):
        if len(self.value) > 255:
            raise

    def as_generic_type(self) -> str:
        return self.value