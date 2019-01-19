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
    def interval(cls) -> int:
        return cls._rule.interval


class cron:  # noqa
    def __init__(
            self,
            rule,
            priority: int = 0,
            cancelled: bool = False,
            right_now: bool = False,
            prefix: str = 'registry',
    ):
        from cronjob.core.registry import Registry
        self.rule = rule
        self.priority = priority
        self.cancelled = cancelled
        self.right_now = right_now
        self.prefix = prefix
        self.registry = Registry.from_settings()

    def __call__(self, func):
        def run(self):
            func()

        cls_name = func.__name__ + '_FuncJob'
        new_cls = type(
            cls_name,
            (BaseJob, ),
            dict(
                rule=self.rule,
                priority=self.priority,
                cancelled=self.cancelled,
                right_now=self.right_now,
                prefix=self.prefix,
                run=run,
            ),
        )
        self.registry._jobs[new_cls.register_key] = new_cls
        self.registry.persist()

        return func
