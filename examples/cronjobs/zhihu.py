from cronjob.apps.spider_app import SpiderJob


class ZhihuSpider(SpiderJob):
    priority = 1
    rule = '* * * * *'

    def run(self):
        self.logger.info('In Zhihu spider')
        response = self.http.get('https://www.zhihu.com')
        self.logger.info(f'zhihu recv {len(response.content)} bytes')
