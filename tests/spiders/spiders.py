from sspider.core.spiders import BaseSpider


class TestSpider(BaseSpider):
    schedule = '* * * * *'

    def crawl(self):
        pass
