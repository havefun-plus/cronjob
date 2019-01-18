import logging
from datetime import datetime

from croniter import croniter

from cronjob.settings import settings
from cronjob.utils.utils import classproperty


class JobError(Exception):
    pass


class BaseJob:
    prefix = f'{settings.DEFAULT_REGISTER_PREFIX}:registry:'
    schedule = ''
    priority = 0
    cancelled = False
    right_now = False

    def __init__(self, *args, **kwargs):
        pass

    def run(self):
        raise NotImplementedError

    @property
    def logger(self):
        logger_name = f'BaseJob.{type(self).__name__}'
        logger = logging.getLogger(logger_name)
        return logging.LoggerAdapter(logger, {'basecls': type(self).__name__})

    def log(self, message, level=logging.DEBUG, **kw):
        self.logger.log(level, message, **kw)

    @classproperty
    def register_key(cls):
        return f'{cls.prefix}{cls.__name__}'

    @classproperty
    def interval(cls):
        # TODO validate schedule string
        now = datetime.now()
        next_time = croniter(cls.schedule, now).get_next(datetime)
        return (next_time - now).seconds
