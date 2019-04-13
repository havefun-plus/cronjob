from abc import ABCMeta, abstractmethod
from typing import Any

from cronjob.types import BASE_QUEUE


class BaseMessage(BASE_QUEUE, metaclass=ABCMeta):
    """
    封装不同的消息队列消息，以提供统一的接口, 目前没用
    """

    @abstractmethod
    def ack(self):
        pass

    @abstractmethod
    def payload(self):
        pass


class BaseQueue(metaclass=ABCMeta):
    """
    封装不同的消息队列，提供统一的接口，以方便支持redis/sqs/rabbitmq等
    """

    def __init__(self, config: dict) -> None:
        self.config = config

    @abstractmethod
    def set_qname(self, qname: str) -> 'BaseQueue':
        pass

    @abstractmethod
    def put(self, payload: bytes) -> Any:
        pass

    @abstractmethod
    def get(self, timeout: float = 3.0) -> str:
        pass
