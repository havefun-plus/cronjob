from sspider.core.spiders import BaseSpider


class ForTestSpider(BaseSpider):
    schedule = '* * * * *'

    def crawl(self):
        pass
