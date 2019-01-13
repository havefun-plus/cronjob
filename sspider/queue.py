import logging
from redis.exceptions import WatchError

from sspider.connection import connection

LOGGER = logging.getLogger('queue')


class DequeueTimeout(Exception):
    pass


class Queue:
    prefix = 'sspider:queue:'

    def __init__(self, name, connection):
        self.connection = connection
        self.name = name
        self.registry_key = f'{self.prefix}{name}'

    @classmethod
    def from_settings(cls):
        return cls('default', connection)

    def enqueue(self, spider_rk) -> bool:
        pipe = self.connection.pipeline()
        try:
            pipe.watch(spider_rk)
            pipe.multi()
            pipe.rpush(self.registry_key, spider_rk)
            pipe.execute()
            return True
        except WatchError:
            LOGGER.error('watch error')
            return False

    def recv(self, timeout=3):
        msg = self.connection.blpop(
            self.registry_key,
            timeout=timeout,
        )
        if not msg:
            raise DequeueTimeout
        _, spider_rk = msg
        return spider_rk.decode()

    def ack(self):
        # TODO
        pass
