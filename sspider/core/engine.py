import threading
import logging
from sspider.core.worker import Worker
from sspider.core.scheduler import Scheduler

LOGGER = logging.getLogger(__name__)


class Engine:
    def __init__(self, worker, scheduler):
        self.worker = worker
        self.scheduler = scheduler

    @classmethod
    def from_settings(cls):
        return cls(
            worker=Worker.from_settings(),
            scheduler=Scheduler.from_settings(),
        )

    def schedule(self):
        LOGGER.info('scheduler start...')
        self.scheduler.run()

    def work(self):
        LOGGER.info('worker start...')
        self.worker.run()

    def run_local(self):
        LOGGER.info('run local mode with thread')
        worker = threading.Thread(target=self.work)
        worker.start()
        scheduler = threading.Thread(target=self.schedule)
        scheduler.start()
