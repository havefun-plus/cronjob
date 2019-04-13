import logging
from collections import OrderedDict
from operator import attrgetter
from typing import AnyStr, Iterable, Optional

from cronjob.apps import BaseJob, JobMeta
from cronjob.settings import settings
from cronjob.utils.loaders import get_all_target_cls

LOGGER = logging.getLogger(__name__)


class Registry:
    """
    所有的Job都注册在这里，是一个单例类，也只初始化一次
    """
    _instance: Optional['Registry'] = None

    def __new__(cls, *args, **kwargs) -> 'Registry':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, module: str) -> None:
        self._initialized: bool
        if self._initialized:
            return
        self._initialized = True
        self.module = module
        self._jobs: dict = OrderedDict()
        self.init_jobs()

    @classmethod
    def from_settings(cls) -> 'Registry':
        return cls(settings.CRONJOBS_MODULE)

    def init_jobs(self) -> None:
        jobs = get_all_target_cls(self.module, BaseJob)
        for job in jobs:
            self.add_job(job)

    def delete_job(self, job: BaseJob) -> bool:
        pass

    def add_job(self, job: BaseJob) -> None:
        """注册Job都要使用这个入口，每次注册都会对所有的job进行排序插入

        :param job:
        :type job: BaseJob
        :rtype: None
        """
        klasses = list(self._jobs.values())
        klasses.append(job)
        klasses.sort(key=attrgetter('priority'), reverse=True)
        for job_cls in klasses:
            self._jobs[job_cls.register_key] = job_cls

    def __getitem__(self, job_rk: AnyStr) -> JobMeta:
        rk = job_rk.decode() if isinstance(job_rk, bytes) else job_rk
        return self._jobs[rk]

    def __contains__(self, job_rk: str) -> bool:
        return job_rk in self._jobs

    def __iter__(self) -> Iterable[AnyStr]:
        yield from self._jobs
