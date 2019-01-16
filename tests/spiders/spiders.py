from sspider.core.spiders import BaseSpider


class ForTestSpider(BaseSpider):
    schedule = '* * * * *'
    right_now = True

    def crawl(self):
        pass
