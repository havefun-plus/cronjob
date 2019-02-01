import logging

from cronjob.utils.utils import classproperty
from cronjob.utils.rule import CronRule

from cronjob.events.event import Event


class JobError(Exception):
    pass


class JobMeta(type):
    """
    所有Job的元类，添加`_rule`和`register_key`，以及event hook
    """

    def __new__(metacls, cls_name, parents, attrs):
        cls = type.__new__(metacls, cls_name, parents, attrs)
        setattr(cls, '_rule', CronRule(attrs['rule']))
        setattr(cls, 'register_key', cls_name)
        for name in ['pre_action', 'post_action', 'err_action']:
            event = Event(name, parents)
            setattr(cls, name, event)
        return cls


class BaseJob(metaclass=JobMeta):
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

    def __call__(self):
        try:
            self.pre_action()
            self.run()
        except Exception:
            self.err_action()
            raise
        else:
            self.post_action()


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

        cls_name = func.__name__
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
        self.registry.add_job(new_cls)
        func.cronjob_cls = new_cls

        return func
