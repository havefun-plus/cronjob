from cronjob.net.proxy import BaseProxy

tests = [
    "http://119.101.116.247:9999",
    "http://121.61.30.117:9999",
    "http://119.101.117.127:9999",
    "http://119.101.116.203:9999",
    "http://119.101.114.52:9999",
]


class IterProxy(BaseProxy):
    def get_proxy_ips(self):
        return tests
