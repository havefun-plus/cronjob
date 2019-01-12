from collections import OrderedDict
from operator import attrgetter

from sspider.utils.loaders import walk_modules, iter_spider_classes
from sspider.settings import settings


class Registry:
    key = 'sspider:registry:'
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(*args, **kwargs)
        return cls._instance

    def __init__(self, module: str, connection: 'Redis'):
        self.module = module
        self.connection = connection
        self.spiders = OrderedDict()
        self.init_spiders()

    @classmethod
    def from_settings(cls):
        return cls(settings.SPIDERS_MODULE)

    def _get_all_spiders(self):
        for module in walk_modules(self.module):
            yield from iter_spider_classes(module)

    def init_spiders(self):
        spiders = list(self._get_all_spiders())
        spiders.sort(key=attrgetter('priority'))
        for spider_cls in spiders:
            self.spiders[spider_cls.registry_key()] = spider_cls

    def persist(self):
        for key, spider_cls in self.spiders.items():
            self.connection.set(key, spider_cls.schedule)

    def remove(self, *args, **kwargs):
        """
        取消某个爬虫
        """
        # TODO

    def add(self, *args, **kwargs):
        """
        添加某个爬虫
        """
        # TODO
