import inspect
from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType
from typing import Iterable, Type

from sspider.core.spiders import BaseSpider


"""
    scrapy
    ~~~~~~~~~~~~~~
    :Copyright (c) Scrapy developers.

"""


# copy from scarpy/utils/spider.py
def iter_spider_classes(module: ModuleType) -> Type:

    for obj in vars(module).values():
        if inspect.isclass(obj) and \
           issubclass(obj, BaseSpider) and \
           obj.__module__ == module.__name__ and \
           not BaseSpider is obj:
            yield obj


# copy from scarpy/utils/misc.py
def walk_modules(path: str) -> Iterable[ModuleType]:
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For example: walk_modules('scrapy.utils')
    """

    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods


def load_object(path: str):
    try:
        dot = path.rindex('.')
    except ValueError:
        raise ValueError("Error loading object '%s': not a full path" % path)

    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)

    try:
        obj = getattr(mod, name)
    except AttributeError:
        raise NameError("Module '%s' doesn't define any object named '%s'" %
                        (module, name))

    return obj
