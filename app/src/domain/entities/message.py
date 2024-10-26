import datetime
from dataclasses import dataclass, field

from domain.values.author import Author
from domain.values.id import UUID7
from domain.entities.base import BaseEntity


@dataclass
class Message(BaseEntity):
    chat_id: UUID7
    content: str
    author: Author
    timestamp: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc))

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id