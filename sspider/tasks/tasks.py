from sspider.queue import DequeueTimeout
from sspider.queue import Queue as RedisQueue
from sspider.registry import Registry
from sspider.tasks import BaseTask, task_queue


class CrawlTask(BaseTask):
    def __init__(self, msg, registry):
        self.msg = msg
        self.registry = registry

    def run(self):
        spider_cls = self.registry[self.msg]
        obj = spider_cls()
        obj.crawl()


class ProducerTask(BaseTask):
    def __init__(self, redis_queue, task_queue, registry):
        self.redis_queue = redis_queue
        self.task_queue = task_queue
        self.registry = registry

    @classmethod
    def from_settings(cls):
        return cls(
            redis_queue=RedisQueue.from_settings(),
            task_queue=task_queue,
            registry=Registry.from_settings(),
        )

    def run(self):
        try:
            self._run()
        except Exception:
            raise
        finally:
            self.repeat()

    def repeat(self):
        self.task_queue.put(self)

    def _run(self):
        try:
            msg = self.redis_queue.recv()
            self.logger.info(f'recv msg: {msg}')
        except DequeueTimeout:
            pass
        else:
            self.task_queue.put(CrawlTask(msg, self.registry))
