import abc
from motor.core import AgnosticClientSession


class BaseMotorRepository(abc.ABC):
    def __init__(self, session: AgnosticClientSession) -> None:
        self._session: AgnosticClientSession = session
