import uuid
from enum import Enum
import uuid6

from domain.values.base import BaseValueObject
from domain.values.id import UUID7, uuid7_gen
from dataclasses import dataclass, field
import abc
from typing import Any, Iterable


@dataclass
class BaseEntity(abc.ABC):
    id: UUID7 = field(default_factory=uuid7_gen, kw_only=True)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id

    def model_dump(self, uuid_conversation: bool = False) -> dict:

        def to_dict_recursive(obj: Any) -> Any:
            if isinstance(obj, BaseValueObject):
                return obj.as_generic_type()
            elif isinstance(obj, BaseEntity):
                return {
                    key: to_dict_recursive(value)
                    for key, value in obj.model_dump().items()
                }
            elif isinstance(obj, Iterable) and not isinstance(obj, str):
                return [to_dict_recursive(item) for item in obj]
            elif isinstance(obj, Enum):
                return obj.value
            elif uuid_conversation and isinstance(obj, uuid.UUID | uuid6.UUID):
                return str(obj)
            else:
                return obj

        return {
            key: to_dict_recursive(value) for key, value in self.__dict__.items()
        }
