import logging

from cronjob.settings import settings
from cronjob.utils.utils import classproperty
from cronjob.utils.rule import CronRule


class JobError(Exception):
    pass


class JobMeta(type):
    def __new__(metacls, cls_name, parents, attrs):
        attrs['_rule'] = CronRule(attrs['rule'])
        prefix = f'{settings.DEFAULT_REGISTER_PREFIX}:{attrs.get("prefix") or parents[0].prefix}:'
        attrs['register_key'] = f'{prefix}{cls_name}'
        return type.__new__(metacls, cls_name, parents, attrs)


class BaseJob(metaclass=JobMeta):
    prefix = 'registry'
    rule = ''
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
    def interval(cls):
        return cls._rule.interval
