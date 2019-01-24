from abc import ABCMeta, abstractmethod
from typing import Any


class BaseMessage(metaclass=ABCMeta):
    @abstractmethod
    def ack(self):
        pass

    @abstractmethod
    def payload(self):
        pass


class BaseQueue(metaclass=ABCMeta):
    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def set_qname(self, qname: str) -> 'BaseQueue':
        pass

    @abstractmethod
    def put(self, payload: bytes) -> Any:
        pass

    @abstractmethod
    def get(self, timeout: float = 3.0):
        pass
