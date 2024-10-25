from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class QueryHandlersNotRegisteredException(LogicException):
    event_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для запроса <{self.event_type}>"


@dataclass(frozen=True, eq=False)
class CommandHandlersNotRegisteredException(LogicException):
    command_type: type

    @property
    def message(self):
        return f"Не удалось найти обработчики для команды <{self.command_type}>"
