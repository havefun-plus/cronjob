import logging
import traceback

import gevent
from gevent.queue import Empty
from gevent.queue import Queue as TaskQueue

from sspider.settings import settings
from sspider.queue import Queue
from sspider.registry import Registry

LOGGER = logging.getLogger(__name__)

tasks = TaskQueue(settings.DEFAULT_WORKER_QUEUE_SIZE)


class Worker:
    def __init__(self, queue: Queue, registry: Registry):
        self.queue = queue
        self.registry = registry

    @classmethod
    def from_settings(cls):
        return cls(
            queue=Queue.from_settings(),
            registry=Registry.from_settings(),
        )

    def _producter(self):
        msg = self.queue.recv()
        tasks.put(msg)

    def producter(self):
        while True:
            try:
                self._producter()
                gevent.sleep(1)
            except Exception as err:
                traceback.print_exc()
                LOGGER.error(f'Producter error: {err}')

    def _consumer(self):
        msg = tasks.get(timeout=3)
        spider_cls = self.registry[msg]
        obj = spider_cls()
        obj.crawl()

    def consumer(self):
        while True:
            try:
                self._consumer()
                gevent.sleep(1)
            except Empty:
                pass
            except Exception as err:
                traceback.print_exc()
                LOGGER.error(f'consumer error: {err}')

    def close(self):
        pass

    def run(self):
        producters = [
            self.producter for _ in range(settings.DEFAULT_PRODUCTER_NUMBER)
        ]
        consumers = [
            self.consumer for _ in range(settings.DEFAULT_CONSUMER_NUMBER)
        ]
        gevent.joinall(
            [gevent.spawn(worker) for worker in [*producters, *consumers]])
