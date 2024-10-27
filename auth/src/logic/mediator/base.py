from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Iterable, Type

from logic.commands.base import BaseCommand, CommandHandler
from logic.exceptions.mediator import (
    CommandHandlersNotRegisteredException,
)


@dataclass(frozen=True, eq=False)
class Mediator[CT: BaseCommand, CR: Any]:
    """
    Класс, который является паттерном медиатора, для связывания команд и их обработчиков, тем самым делая их атомарными.
     Одна команда может иметь множество обработчиков
    """
    commands_map: dict[CT, list[CommandHandler]] = field(default_factory=lambda: defaultdict(list), kw_only=True)

    def register_command(self, command: Type[CT], command_handlers: Iterable[CommandHandler[CT, CR]]):
        """
        Добавление новой команды для обработки
        :param command: Команда
        :param command_handlers: список обработчиков
        :return:
        """
        self.commands_map[command].extend(command_handlers)

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        """
        Обработчик команды, который асинхронно вызывает выполнение всех обработчиков
        :param command: Команда
        :return: Список результата выполнения каждого обработчика
        """
        command_type = command.__class__
        handlers: list[CommandHandler] = self.commands_map.get(command_type)
        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)
        return [await handler.handle(command=command) for handler in handlers]
