import random
from typing import Iterable
from cronjob.apps.spider_app.proxy import BaseProxy
"""
使用代理需要配置
    1. ENABLE_PROXY = True
    2. PROXY_CLASS = 'cronjobs.proxy.IterProxy'
"""

tests = [
    "http://119.101.116.247:9999",
    "http://121.61.30.117:9999",
    "http://119.101.117.127:9999",
    "http://119.101.116.203:9999",
    "http://119.101.114.52:9999",
]


# 继承BaseProxy
class IterProxy(BaseProxy):
    # 实现这个方法，
    def get_proxy_ips(self) -> Iterable[str]:
        return tests


class RandomProxy(BaseProxy):
    # 或者直接实现run方法
    def run(self):
        return random.choice(tests)
