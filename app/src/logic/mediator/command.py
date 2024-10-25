from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)


@dataclass(frozen=True, eq=False)
class CommandMediator(ABC):
    commands_map: dict = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_command(self, command, command_handlers): ...
    @abstractmethod
    async def handle_command(self, command) -> Iterable: ...
