import logging
from collections import OrderedDict
from operator import attrgetter
from typing import AnyStr

from redis.exceptions import WatchError

from sspider.connection import connection
from sspider.core.spiders import BaseSpider
from sspider.settings import settings
from sspider.utils.loaders import iter_target_classes, walk_modules, get_all_target_cls

LOGGER = logging.getLogger('registry')


class Registry:
    prefix = 'sspider:registry:'
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, module: str, connection):
        self.module = module
        self.connection = connection
        self._spiders = OrderedDict()
        self.working_key = f'{self.prefix}working'
        self.deleted_key = f'{self.prefix}deleted'
        self.init_spiders()
        self.persist()

    @classmethod
    def from_settings(cls):
        return cls(
            settings.SPIDERS_MODULE,
            connection=connection,
        )

    def init_spiders(self):
        spiders = list(get_all_target_cls(self.module, BaseSpider))
        spiders.sort(key=attrgetter('priority'))
        for spider_cls in spiders:
            self._spiders[spider_cls.registry_key()] = spider_cls

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
                pass

    def delete(self, spider_rk: str):
        self.transaction(self._delete, spider_rk)
        LOGGER.info(f'unregister {spider_rk} success')

    def _delete(self, pipe, spider_rk: str):
        pipe.sadd(self.deleted_key, spider_rk)
        pipe.srem(self.working_key, spider_rk)

    def add(self, spider_rk: str):
        self.transaction(self._add, spider_rk)
        LOGGER.info(f'register {spider_rk} success')

    def _add(self, pipe, spider_rk: str):
        pipe.sadd(self.working_key, spider_rk)
        pipe.srem(self.deleted_key, spider_rk)

    def isdeleted(self, spider_rk: str):
        self.connection.sismember(self.deleted_key, spider_rk)

    def persist(self):
        for key, spider_cls in self._spiders.items():
            if not self.isdeleted(key):
                self.add(key)

    def __contains__(self, spider_rk: str):
        if self.isdeleted(spider_rk):
            return False
        return self.connection.sismember(self.working_key, spider_rk)

    def __getitem__(self, spider_rk: AnyStr):
        if isinstance(spider_rk, bytes):
            spider_rk = spider_rk.decode()
        if not self.isdeleted(spider_rk):
            return self._spiders[spider_rk]

    def __setitem__(self, spider_rk, value):
        raise AttributeError

    def __iter__(self):
        workings = self.connection.smembers(self.working_key)
        for spider_rk in workings:
            if not self.isdeleted(spider_rk):
                yield spider_rk
