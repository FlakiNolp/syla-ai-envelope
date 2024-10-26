import abc


class BaseMessagesRepository(abc.ABC):
    @abc.abstractmethod
    def add_message(self): ...
