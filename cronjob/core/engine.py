import logging
import signal
from multiprocessing import Process
from threading import Thread

import gevent
from cronjob.core.scheduler import Scheduler
from cronjob.core.worker import Worker
from cronjob.utils.utils import capture_greenlet_exc

LOGGER = logging.getLogger(__name__)


class Engine:
    def __init__(self, worker, scheduler) -> None:
        self.worker = worker
        self.scheduler = scheduler

    @classmethod
    def from_settings(cls) -> 'Engine':
        return cls(
            worker=Worker(),
            scheduler=Scheduler.from_settings(),
        )

    def schedule(self) -> None:
        LOGGER.info('scheduler start...')
        self.scheduler.run()

    def work(self) -> None:
        LOGGER.info('worker start...')
        gevent.signal(signal.SIGQUIT, gevent.kill)
        self.worker.start()
        self.worker.link_exception(capture_greenlet_exc)
        self.worker.join()

    def run_local(self, process=False, worker_num=1) -> None:
        LOGGER.info(f'run local mode with Process = {process}')
        Job = Process if process else Thread
        jobs = [Job(target=self.work) for i in range(worker_num)]
        for job in jobs:
            job.start()
        self.schedule()
