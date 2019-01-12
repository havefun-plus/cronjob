from redis.exceptions import WatchError

from sspider.connection import connection

# TODO ack


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
            return False

    def recv(self, timeout=3):
        return self.connection.blpop(
            self.registry_key,
            timeout=timeout,
        )

    def ack(self):
        # TODO
        pass
