from cronjob.apps import BaseJob
from cronjob.net import http


class SpiderJob(BaseJob):
    rule = ''
    priority = 0
    cancelled = False
    right_now = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http = http

    def run(self):
        raise NotImplementedError
