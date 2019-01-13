from threading import Thread
from multiprocessing import Process
import logging
from sspider.core.worker import Worker
from sspider.core.scheduler import Scheduler

LOGGER = logging.getLogger('engine')


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

    def run_local(self, process=False, worker_num=1):
        LOGGER.info(f'run local mode with Process = {process}')
        Job = Process if process else Thread
        jobs = [Job(target=self.work) for i in range(worker_num)]
        for job in jobs:
            job.start()
        scheduler = Job(target=self.schedule)
        scheduler.start()
