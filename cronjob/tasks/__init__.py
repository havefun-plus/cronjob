import logging
from gevent.queue import Queue as TaskQueue

from cronjob.settings import settings

task_queue = TaskQueue(settings.DEFAULT_TASK_QUEUE_SIZE)


class BaseTask:
    def run(self):
        raise NotImplementedError

    @property
    def logger(self):
        logger_name = f'BaseTask.{type(self).__name__}'
        logger = logging.getLogger(logger_name)
        return logging.LoggerAdapter(logger, {'basecls': type(self).__name__})

    def log(self, message, level=logging.DEBUG, **kw):
        self.logger.log(level, message, **kw)
