### 配置文件

目前需要在项目根目录`export PYTHONPATH=.`

通过环境变量`SSPIDER_SETTINGS`指定配置文件, 配置见`settings.example.py`, 也可不指定使用默认配置

### 爬虫脚本

所有爬虫默认放在工程根目录下的`spiders`文件夹

1. 所有爬虫都需要继承`sspider.core.spiders.BaseSpider`
2. 实现crawl方法, 在这个方法内可以随便折腾
3. 复制类属性`schedule`, 用法同[crontab](https://en.wikipedia.org/wiki/Cron), 比如`3,15 8-11 * * *`在上午8点到11点的第3和第15分钟执行。
3. 发送请求建议使用`self.http`, 也可以使用`requests`, 这样的话会有一些配置失效, 比如重试， 代理。`self.http`返回的也是`requests.Response`
2. 打印日志最好使用`self.logger`或者`self.log`

### 启动

#### 1. 主从运行

* 启动主节点: `sspider runmaster`
* 启动从节点: `sspider runworker`

#### 2. 单节点运行（目前不可用，后续修复）

默认线程模式：

* `sspider runlocal`  默认一个线程调度任务，一个线程爬取


进程模式:

* `sspider runlocal --process`, 一个进程调度，默认一个进程爬取

可以加worker:

* `sspider runlocal --process --num 2`, 一个进程调度，两个进程爬取
