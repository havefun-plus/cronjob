import logging

from cronjob.core.registry import Registry
from cronjob.queue import DequeueTimeout
from cronjob.queue import Queue as RedisQueue
from cronjob.tasks import BaseTask, task_queue

LOGGER = logging.getLogger(__name__)


class NormalTask(BaseTask):
    def __init__(self, job_cls: 'BaseJob') -> None:
        self.job_cls = job_cls

    def run(self) -> None:
        LOGGER.info(f'{self.job_cls.__name__} run')
        obj = self.job_cls()
        obj.run()


class ProducerTask(BaseTask):
    def __init__(
            self,
            redis_queue: 'cronjob.queue.Queue',
            task_queue: 'gevent.queue.Queue',
            registry: 'Registry',
    ) -> None:
        self.redis_queue = redis_queue
        self.task_queue = task_queue
        self.registry = registry

    @classmethod
    def from_settings(cls) -> 'ProducerTask':
        return cls(
            redis_queue=RedisQueue.from_settings(),
            task_queue=task_queue,
            registry=Registry.from_settings(),
        )

    def run(self) -> None:
        try:
            self._run()
        except Exception:
            raise
        finally:
            self.repeat()

    def repeat(self) -> None:
        self.task_queue.put(self)

    def _run(self) -> None:
        try:
            msg = self.redis_queue.recv()
            self.logger.info(f'recv msg: {msg}')
            job_cls = self.registry[msg]
        except DequeueTimeout:
            pass
        else:
            self.task_queue.put(NormalTask(job_cls))
