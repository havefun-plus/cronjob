from sspider.core.spiders import BaseSpider


class ForTestSpider(BaseSpider):
    schedule = '* * * * *'

    def crawl(self):
        pass


class ForTestSpider2(BaseSpider):
    schedule = '* * * * *'

    def crawl(self):
        pass
