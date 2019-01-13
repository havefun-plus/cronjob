from sspider.core.spiders import BaseSpider


class ZhihuSpider(BaseSpider):
    priority = 1
    schedule = '* * * * *'

    def crawl(self):
        self.logger.info('In Zhihu spider')
        response = self.http.get('https://www.zhihu.com')
        self.logger.info(f'zhihu recv {len(response.content)} bytes')
