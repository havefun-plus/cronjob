import logging
import sched
import time
import traceback
from typing import Callable

from cronjob.core.registry import Registry
from cronjob.queues import get_queue_client
from cronjob.settings import settings

LOGGER = logging.getLogger(__name__)


class Scheduler:
    def __init__(self, registry, queue) -> None:
        self.registry = registry
        self.queue = queue
        self._scheduler = sched.scheduler(time.time, time.sleep)

    @classmethod
    def from_settings(cls) -> 'Scheduler':
        queue = get_queue_client(settings.QUEUE_CONFIG)
        queue.set_qname(settings.JOB_QUEUE_NAME)
        return cls(registry=Registry.from_settings(), queue=queue)

    def periodic(self, func: Callable[['BaseJob'], None],
                 job_cls: 'BaseJob') -> None:
        if not job_cls.cancelled:
            interval = job_cls.interval
            self._scheduler.enter(
                interval,
                job_cls.priority,
                self.periodic,
                (func, job_cls),
            )
            if job_cls.right_now:
                func(job_cls)
            else:
                job_cls.right_now = True

    def schedule_all(self) -> None:
        LOGGER.info('schedule all...')
        for job_rk in self.registry:
            job_cls = self.registry[job_rk]
            self.periodic(self.schedule, job_cls)

    def schedule(self, job_cls: 'BaseJob') -> None:
        LOGGER.info(f'schedule {job_cls.__name__}')
        # TODO handle enqueue failed
        self.queue.put(job_cls.register_key.encode())

    def _run(self) -> None:
        try:
            self.schedule_all()
            self._scheduler.run()
        except Exception:
            LOGGER.error('scheduler error')
            traceback.print_exc()
            time.sleep(1)
        LOGGER.error('scheduler stop')

    def run(self):
        while True:
            self._run()
