from .redis_queue import RedisQueue
from .local_queue import ThreadQueue, ProcessQueue
from .base import BaseQueue
from .exceptions import DequeueTimeout

registry = {
    klass.queue_type: klass
    for klass in [RedisQueue, ThreadQueue, ProcessQueue]
    if klass and hasattr(klass, 'queue_type')
}

__all__ = ['get_queue_client', 'DequeueTimeout']


def get_queue_client(config: dict) -> BaseQueue:
    """
    根据配置实例化不同的queue
    """
    return registry[config['queue_type']](config['config'])
