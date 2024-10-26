from enum import EnumMeta

from auth.src.domain.values.base import BaseValueObject


class Author(BaseValueObject, metaclass=EnumMeta):
    def validate(self):
        pass

    def as_generic_type(self) -> str:
        pass

    user = "user"
    chatbot = "chatbot"
