from redis.exceptions import WatchError
from sspider.connection import connection


class Queue:
    prefix = 'sspider:queue:'

    def __init__(self, name, connection):
        self.connection = connection
        self.name = name
        self.registry_key = f'{self.prefix}{name}'

    @classmethod
    def from_settings(cls):
        return cls('default', connection)

    def enqueue(self, spider_registry_key: str) -> bool:
        pipe = self.connection.pipeline()
        try:
            pipe.watch(spider_registry_key)
            pipe.multi()
            pipe.rpush(self.registry_key, spider_registry_key)
            pipe.execute()
            return True
        except WatchError:
            return False
