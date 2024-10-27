from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(frozen=True, eq=False)
class AnswerGenerationException(LogicException):
    text: str

    @property
    def message(self):
        return f"Не получилось сгенерировать ответ на сообщение <{self.text}>"
