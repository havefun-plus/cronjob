from .redis_queue import RedisQueue
from .base import BaseQueue
from .exceptions import DequeueTimeout

registry = {
    klass.queue_type: klass
    for klass in [RedisQueue] if klass and hasattr(klass, 'queue_type')
}

__all__ = ['get_queue_client', 'DequeueTimeout']


def get_queue_client(config: dict) -> BaseQueue:
    return registry[config['queue_type']](config['config'])
