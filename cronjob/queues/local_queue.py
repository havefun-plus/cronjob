from multiprocessing import Queue as PQueue
from queue import Empty
from queue import Queue as TQueue
from typing import Any, AnyStr

from .base import BaseQueue
from .exceptions import DequeueTimeout


class LocalQueue(BaseQueue):
    def __init__(self, config: dict, queue) -> None:
        super().__init__(config)
        self.queue = queue

    def set_qname(self, qname: str) -> 'BaseQueue':
        pass

    def put(self, payload: bytes) -> Any:
        self.queue.put(payload)

    def get(self, timeout: float = 3) -> AnyStr:
        try:
            return self.queue.get(timeout=3)
        except Empty:
            raise DequeueTimeout


class ThreadQueue(LocalQueue):
    queue_type = 'thread'

    def __init__(self, config: dict, queue=TQueue()) -> None:
        super().__init__(config, queue)


class ProcessQueue(LocalQueue):
    queue_type = 'process'

    def __init__(self, config: dict, queue=PQueue()) -> None:
        super().__init__(config, queue)
