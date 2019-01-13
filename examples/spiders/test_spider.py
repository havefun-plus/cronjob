from sspider.core.spiders import BaseSpider


class TestSpider(BaseSpider):
    priority = 1
    schedule = '* * * * *'

    def crawl(self):
        self.logger.info('IN TESTSPIDER')
