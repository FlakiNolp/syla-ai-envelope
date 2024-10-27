from dataclasses import dataclass
import abc
from typing import Any


@dataclass(frozen=True)
class BaseCommand(abc.ABC):
    """
    Базовый класс команды
    """


@dataclass(frozen=True)
class CommandHandler[CT: BaseCommand, CR: Any](abc.ABC):
    """
    Базовый класс обработчика команды
    """
    @abc.abstractmethod
    async def handle(self, command: CT) -> CR:
        """
        Обрабатывает команду и возвращает результат
        :param command: Класс команды
        :return: Результаты обработки
        """
