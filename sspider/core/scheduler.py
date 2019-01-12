import time
import sched
import logging
import threading

from sspider.registry import Registry
from sspider.queue import Queue

LOGGER = logging.getLogger(__name__)


class Scheduler:
    def __init__(self):
        self.registry = Registry()
        self.queue = Queue.from_settings()
        self._scheduler = sched.scheduler(time.time, time.sleep)

    def periodic(self, func, spider_cls):
        if not spider_cls.canceled:
            LOGGER.debug(f'schedule {spider_cls.__name__}')
            self._scheduler.enter(
                60,  # interval
                99,  # priority
                self.periodic,
                (func, spider_cls),
            )

            func(spider_cls)

    def schedule_all(self):
        LOGGER.info('schedule all...')
        for spider_rk in self.registry:
            self.periodic(self.schedule, self.registry[spider_rk])

    def schedule(self, spider_cls):
        if spider_cls.need_schedule():
            self.queue.enqueue(spider_cls.registry_key)

    def run(self):
        t = threading.Thread(target=self._scheduler.run)
        t.start()
        t.join()
