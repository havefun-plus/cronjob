from sspider.core.spiders import BaseSpider


class MultiSpider(BaseSpider):
    priority = 1
    schedule = '* * * * *'

    def crawl(self):
        self.logger.info('IN second spider')
