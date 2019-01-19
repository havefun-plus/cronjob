from cronjob.apps.spider_app import SpiderJob


class BaiduSpider(SpiderJob):
    rule = '5s'

    def run(self):
        self.logger.info('In Baidu spider')
        response = self.http.get('https://www.baidu.com')
        self.logger.info(f'Baidu recv {len(response.content)} bytes')
