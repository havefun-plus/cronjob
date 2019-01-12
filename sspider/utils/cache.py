import logging
from collections import OrderedDict

import socket

LOGGER = logging.getLogger(__name__)


class LocalCache(OrderedDict):

    def __init__(self, limit=None):
        super().__init__()
        self.limit = limit

    def __setitem__(self, key, value):
        while len(self) >= self.limit:
            self.popitem(last=False)
        super().__setitem__(key, value)


dns_cache = LocalCache(10000)

# 因为爬虫需要长时间运行，而dns cache容易出错，所以dns cache 并未使用


def set_dns_cache():

    def _getaddrinfo(*args, **kwargs):
        if args in dns_cache:
            LOGGER.debug(f'Use dns cache {args}:{dns_cache[args]}')
            return dns_cache[args]

        else:
            LOGGER.debug(f'Without dns cache {args}')
            dns_cache[args] = socket._getaddrinfo(*args, **kwargs)
            return dns_cache[args]

    if not hasattr(socket, '_getaddrinfo'):
        socket._getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = _getaddrinfo
