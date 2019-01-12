from typing import Iterable


class ProxyError(Exception):
    pass


class BaseProxy:
    def __init__(self):
        self.proxies = []

    def get_proxy_ips(self) -> Iterable[str]:
        raise NotImplementedError

    def get(self) -> str:
        if not self.proxies:
            self.proxies = self.get_proxy_ips()
        if self.proxies:
            return self.proxies.pop()
        raise ProxyError('Proxy pool is empty!')
