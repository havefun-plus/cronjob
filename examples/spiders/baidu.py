from sspider.core.spiders import BaseSpider


class BaiduSpider(BaseSpider):
    schedule = '* * * * *'

    def crawl(self):
        self.logger.info('In Baidu spider')
        response = self.http.get('https://www.baidu.com')
        self.logger.info(f'Baidu recv {len(response.content)} bytes')
