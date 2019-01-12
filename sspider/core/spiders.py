import logging

from sspider.net import http


class SpiderError(Exception):
    pass


class BaseSpider:
    key = 'sspider:spider:'
    schedule = ''
    priority = 0

    def __init__(self, *args, **kwargs):
        self.http = http

    def start_requests(self):
        raise NotImplementedError

    @classmethod
    def registry_key(cls):
        return f'{cls.key}{cls.__name__}'

    @property
    def logger(self):
        logger_name = f'BaseSpider.{type(self).__name__}'
        logger = logging.getLogger(logger_name)
        return logging.LoggerAdapter(logger, {'spider': type(self).__name__})

    def log(self, message, level=logging.DEBUG, **kw):
        self.logger.log(level, message, **kw)
