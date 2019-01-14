import logging
import sched
import time
import traceback

from sspider.queue import Queue
from sspider.registry import Registry

LOGGER = logging.getLogger('scheduler')


class Scheduler:
    def __init__(self, registry, queue):
        self.registry = registry
        self.queue = queue
        self._scheduler = sched.scheduler(time.time, time.sleep)

    @classmethod
    def from_settings(cls):
        return cls(
            registry=Registry.from_settings(),
            queue=Queue.from_settings(),
        )

    def periodic(self, func, spider_cls):
        if not spider_cls.canceled:
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
            # TODO handler enqueue failed
            LOGGER.info(f'schedule {spider_cls.__name__}')
            self.queue.enqueue(spider_cls.registry_key())

    def _run(self):
        try:
            self.schedule_all()
            self._scheduler.run()
        except Exception:
            LOGGER.error('scheduler error')
            traceback.print_exc()
            time.sleep(1)
        # LOGGER.error('scheduler stop')

    def run(self):
        while True:
            self._run()

    def restart(self):
        # TODO
        pass
