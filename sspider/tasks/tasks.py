import traceback

from sspider.tasks import BaseTask
from sspider.queue import Queue as RedisQueue
from sspider.queue import DequeueTimeout
from sspider.registry import Registry
from sspider.tasks import task_queue


class CrawlTask(BaseTask):
    def __init__(self, msg):
        self.msg = msg
        self.registry = Registry.from_settings()

    def run(self):
        spider_cls = self.registry[self.msg]
        obj = spider_cls()
        obj.crawl()


class ProducterTask(BaseTask):
    def __init__(self, redis_queue, task_queue):
        self.redis_queue = redis_queue
        self.task_queue = task_queue

    @classmethod
    def from_settings(cls):
        return cls(
            redis_queue=RedisQueue.from_settings(),
            task_queue=task_queue,
        )

    def run(self):
        try:
            self._producter()
        except Exception as err:
            self.logger.error(f'error: {err}')
            traceback.print_exc()
        else:
            self.task_queue.put(self)

    def _producter(self):
        try:
            msg = self.redis_queue.recv()
            self.logger.info(f'recv msg: {msg}')
        except DequeueTimeout:
            pass
        else:
            self.task_queue.put(CrawlTask(msg))
