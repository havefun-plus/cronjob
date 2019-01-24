import logging
from typing import AnyStr

from redis import StrictRedis
from redis.exceptions import WatchError

from .base import BaseQueue
from .exceptions import DequeueTimeout

LOGGER = logging.getLogger(__name__)


class RedisQueue(BaseQueue):
    queue_type = 'redis'

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.connection = StrictRedis(**self.config)

    def set_qname(self, qname: str) -> 'ReidsQueue':
        self.qname = qname
        return self

    def put(self, payload: bytes) -> bool:
        return self._put(self.qname, payload)

    def _put(self, qname: str, payload: bytes) -> bool:
        pipe = self.connection.pipeline()
        try:
            pipe.watch(qname)
            pipe.multi()
            pipe.rpush(qname, payload)
            pipe.execute()
            return True
        except WatchError:
            LOGGER.error(f'watch error queue name: {qname}')
            return False

    def get(self, timeout: float = 3) -> AnyStr:
        return self._get(self.qname, timeout)

    def _get(self, qname: str, timeout: float = 3) -> AnyStr:
        msg = self.connection.blpop(
            self.qname,
            timeout=timeout,
        )
        if not msg:
            raise DequeueTimeout
        _, job_rk = msg
        return job_rk.decode()
