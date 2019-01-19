from cronjob.apps.spider_app import SpiderJob


class BaiduSpider(SpiderJob):
    #  设置执行时间, 语法参考[Cron](https://en.wikipedia.org/wiki/Cron)
    rule = '1m'  # 每隔一分钟执行一次

    # 也可以使用下面的方法
    # rule = '3s' # 每隔3秒执行一次
    # rule = '1m3s'  # 每隔1分3秒执行一次
    # rule = '1h5s'  # 每隔1小时5秒执行一次
    # rule = '2h1m3s'  # 每隔2小时1分3秒执行一次

    def run(self):
        """
        因为使用gevent，所有的请求都是异步的
        """
        # 打印日志最好使用self.logger或者self.log
        self.logger.info('In Baidu spider')

        # 爬虫类的请求最好使用self.http， 用法同requests
        # 里面封装了重试，代理，user-agent
        # 代理配置参考`examples/cronjobs/proxy.py`
        response = self.http.get('https://www.baidu.com')

        self.logger.info(f'Baidu recv {len(response.content)} bytes')
