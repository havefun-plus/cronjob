import logging
from collections import OrderedDict
from operator import attrgetter
from typing import AnyStr

from redis.exceptions import WatchError

from cronjob.apps import BaseJob
from cronjob.connection import connection
from cronjob.settings import settings
from cronjob.utils.loaders import get_all_target_cls

LOGGER = logging.getLogger(__name__)


class Registry:
    prefix = f'{settings.DEFAULT_REGISTER_PREFIX}:registry:'
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, module: str, connection):
        self.module = module
        self.connection = connection
        self._jobs = OrderedDict()
        self.working_key = f'{self.prefix}working'
        self.deleted_key = f'{self.prefix}deleted'
        self.init_jobs()
        self.persist()

    @classmethod
    def from_settings(cls):
        return cls(
            settings.CRONJOBS_MODULE,
            connection=connection,
        )

    def init_jobs(self):
        jobs = list(get_all_target_cls(self.module, BaseJob))
        jobs.sort(key=attrgetter('priority'), reverse=True)
        for job_cls in jobs:
            self._jobs[job_cls.register_key] = job_cls

    def transaction(self, func, *args):
        pipe = self.connection.pipeline()
        while True:
            try:
                pipe.watch(self.deleted_key, self.working_key)
                pipe.multi()
                func(pipe, *args)
                pipe.execute()
                return
            except WatchError:
                LOGGER.debug(f'watch error {args}')

    def delete(self, job_rk: str):
        self.transaction(self._delete, job_rk)
        LOGGER.info(f'unregister {job_rk} success')

    def _delete(self, pipe, job_rk: str):
        pipe.sadd(self.deleted_key, job_rk)
        pipe.srem(self.working_key, job_rk)

    def add(self, job_rk: str):
        self.transaction(self._add, job_rk)
        LOGGER.info(f'register {job_rk} success')

    def _add(self, pipe, job_rk: str):
        pipe.sadd(self.working_key, job_rk)
        pipe.srem(self.deleted_key, job_rk)

    def isdeleted(self, job_rk: str):
        return self.connection.sismember(self.deleted_key, job_rk)

    def persist(self):
        for key, job_cls in self._jobs.items():
            if not self.isdeleted(key):
                self.add(key)

    def __contains__(self, job_rk: str):
        if self.isdeleted(job_rk):
            return False
        return self.connection.sismember(self.working_key, job_rk)

    def __getitem__(self, job_rk: AnyStr):
        if isinstance(job_rk, bytes):
            job_rk = job_rk.decode()
        if not self.isdeleted(job_rk):
            return self._jobs[job_rk]

    def __setitem__(self, job_rk, value):
        raise AttributeError

    def __iter__(self):
        workings = self.connection.smembers(self.working_key)
        for job_rk in workings:
            if not self.isdeleted(job_rk):
                yield job_rk
