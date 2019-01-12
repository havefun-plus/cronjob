import logging

from net import http


class SpiderError(Exception):
    pass


class BaseSpider:
    timer = ''

    def __init__(self, article: dict) -> None:
        self.article = article
        self.http = http

    def start_requests(self):
        raise NotImplementedError

    @property
    def logger(self):
        logger_name = f'BaseSpider.{type(self).__name__}'
        logger = logging.getLogger(logger_name)
        return logging.LoggerAdapter(logger, {'spider': type(self).__name__})

    def log(self, message, level=logging.DEBUG, **kw):
        self.logger.log(level, message, **kw)
