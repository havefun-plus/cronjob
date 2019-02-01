import logging

from cronjob.core.registry import Registry
from cronjob.queues import DequeueTimeout, get_queue_client
from cronjob.settings import settings
from cronjob.tasks import BaseTask, task_queue

LOGGER = logging.getLogger(__name__)


class NormalTask(BaseTask):
    """
    这个类是对job的封装
    """

    def __init__(self, job_cls: 'BaseJob') -> None:
        self.job_cls = job_cls

    def run(self) -> None:
        LOGGER.info(f'{self.job_cls.__name__} run')
        obj = self.job_cls()
        obj()


class ProducerTask(BaseTask):
    """
    这个task会不停的从msg_queue里面取消息，实例化任务，扔进task_queue
    """

    def __init__(
            self,
            msg_queue: 'cronjob.queues.BaseQueue',
            task_queue: 'gevent.queue.Queue',
            registry: 'Registry',
    ) -> None:
        self.msg_queue = msg_queue
        self.task_queue = task_queue
        self.registry = registry

    @classmethod
    def from_settings(cls) -> 'ProducerTask':
        queue = get_queue_client(settings.QUEUE_CONFIG)
        queue.set_qname(settings.JOB_QUEUE_NAME)
        return cls(
            msg_queue=queue,
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
            msg = self.msg_queue.get()
            self.logger.info(f'recv msg: {msg}')
            job_cls = self.registry[msg]
        except DequeueTimeout:
            pass
        else:
            self.task_queue.put(NormalTask(job_cls))
