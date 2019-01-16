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
    right_now = False

    def __init__(self, *args, **kwargs):
        self.http = http

    def crawl(self):
        raise NotImplementedError

    @property
    def logger(self):
        logger_name = f'BaseSpider.{type(self).__name__}'
        logger = logging.getLogger(logger_name)
        return logging.LoggerAdapter(logger, {'basecls': type(self).__name__})

    def log(self, message, level=logging.DEBUG, **kw):
        self.logger.log(level, message, **kw)

    @classmethod
    def registry_key(cls):
        return f'{cls.prefix}{cls.__name__}'

    @classmethod
    def get_interval(cls):
        now = datetime.now()
        next_time = croniter(cls.schedule, now).get_next(datetime)
        return (next_time - now).seconds
