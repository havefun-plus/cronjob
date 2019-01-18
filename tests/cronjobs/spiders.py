from cronjob.apps.spider_app import SpiderJob


class ForTestSpider(SpiderJob):
    schedule = '* * * * *'
    right_now = True

    def run(self):
        pass
