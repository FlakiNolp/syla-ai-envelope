from enum import Enum

from domain.values.base import BaseValueObject


class Author(Enum):
    user = "user"
    ai = "ai"
