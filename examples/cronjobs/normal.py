import datetime
import logging

from cronjob.apps import BaseJob


class NormalJob(BaseJob):
    #  设置执行时间, 语法参考[Cron](https://en.wikipedia.org/wiki/Cron)
    rule = '* * * * *'  # 每隔一分钟执行一次

    # rule = '1,31 * * * *'  # 每小时钟的第1和第15分钟执行一次
    # rule = '1,31 10-20 */3  *  *' # 每隔三天的10点到20点第1和第31分钟执行一次

    # 也可以使用下面的方法
    # rule = '3s' # 每隔3秒执行一次
    # rule = '1m3s'  # 每隔1分3秒执行一次
    # rule = '1h5s'  # 每隔1小时5秒执行一次
    # rule = '2h1m3s'  # 每隔2小时1分3秒执行一次

    def run(self):
        self.logger.info('Normal job run')
        infos = dict(msg='test', time=datetime.datetime.now())
        self.log(infos, level=logging.DEBUG)
