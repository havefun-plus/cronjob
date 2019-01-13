import logging
from datetime import datetime

from croniter import croniter

from sspider.net import http


class SpiderError(Exception):
    pass


class BaseSpider:
    prefix = 'sspider:registry:'
    schedule = ''
    priority = 0
    canceled = False
    last_schedule = datetime.now()

    def __init__(self, *args, **kwargs):
        self.http = http

    def crawl(self):
        raise NotImplementedError

    @property
    def logger(self):
        logger_name = f'BaseSpider.{type(self).__name__}'
        logger = logging.getLogger(logger_name)
        return logging.LoggerAdapter(logger, {'spider': type(self).__name__})

    def log(self, message, level=logging.DEBUG, **kw):
        self.logger.log(level, message, **kw)

    @classmethod
    def registry_key(cls):
        return f'{cls.prefix}{cls.__name__}'

    @classmethod
    def need_schedule(cls):
        iter_job = croniter(cls.schedule, cls.last_schedule)
        next_job = iter_job.get_next(datetime)
        now = datetime.now()
        if next_job.strftime('%Y%m%d%H%M') == now.strftime('%Y%m%d%H%M'):
            cls.last_schedule = now
            return True
        return False
