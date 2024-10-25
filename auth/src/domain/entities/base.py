from copy import copy
from dataclasses import dataclass, field
import abc
from typing import Any, Iterable

import uuid6


@dataclass
class BaseEntity(abc.ABC):
    id: uuid6.UUID = field(default_factory=uuid6.uuid8, kw_only=True)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id

    def model_dump(self) -> dict:

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
            else:
                return obj

        return {
            key: to_dict_recursive(value) for key, value in self.__dict__.items()
        }
