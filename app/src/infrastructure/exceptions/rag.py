from dataclasses import dataclass

from infrastructure.exceptions.base import InfrastructureException


@dataclass(frozen=True, eq=False)
class RagRequestException(InfrastructureException):
    text: str

    @property
    def message(self) -> str:
        return f"Не удалось сгенерировать ответ для <{self.text}>"
