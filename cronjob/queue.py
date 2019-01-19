import logging

from redis.exceptions import WatchError

from cronjob.broker import connection
from cronjob.settings import settings

LOGGER = logging.getLogger(__name__)


class DequeueTimeout(Exception):
    pass


class Queue:
    prefix = f'{settings.DEFAULT_REGISTER_PREFIX}:queue:'

    def __init__(self, name, connection):
        self.connection = connection
        self.name = name
        self.register_key = f'{self.prefix}{name}'

    @classmethod
    def from_settings(cls):
        return cls('default', connection)

    def enqueue(self, job_rk) -> bool:
        pipe = self.connection.pipeline()
        try:
            pipe.watch(job_rk)
            pipe.multi()
            pipe.rpush(self.register_key, job_rk)
            pipe.execute()
            return True
        except WatchError:
            LOGGER.error('watch error')
            return False

    def recv(self, timeout=3):
        msg = self.connection.blpop(
            self.register_key,
            timeout=timeout,
        )
        if not msg:
            raise DequeueTimeout
        _, job_rk = msg
        return job_rk.decode()

    def ack(self):
        # TODO
        pass
