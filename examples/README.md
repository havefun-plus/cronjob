### 配置文件

目前需要在项目根目录`export PYTHONPATH=.`

通过环境变量`CRONJOB_SETTINGS`指定配置文件, 配置见`settings.example.py`, 也可不指定使用默认配置

### 定时任务脚本

所有定时任务默认放在工程根目录下的`cronjobs`文件夹


以定时爬虫脚本举例

1. 爬虫需要继承`cronjob.apps.spider_app.SpiderJob`, 也可以继承`cronjob.apps.BaseJob`
2. 实现`run`方法, 在这个方法内可以随便折腾
3. 赋值类属性`schedule`, 用法同[crontab](https://en.wikipedia.org/wiki/Cron), 比如`3,15 8-11 * * *`在上午8点到11点的第3和第15分钟执行。
3. 发送请求建议使用`self.http`, 也可以使用`requests`, 这样的话会有一些配置失效, 比如重试， 代理。`self.http`返回的也是`requests.Response`
2. 打印日志最好使用`self.logger`或者`self.log`

### 使用代理

1. 继承`from cronjob.net.proxy import BaseProxy`, 实现`get_proxy_ips`方法，返回可迭代的代理`ip`, 参考`example.proxy.Iterproxy`， 也可以直接实现`get`方法，每次返回一次`ip`
2. 在配置文件中指定代理类`PROXY_CLASS`


### 启动

#### 1. 主从运行

* 启动主节点: `cronjob runmaster`
* 启动从节点: `cronjob runworker`

#### 2. 单节点运行

默认线程模式：

* `cronjob runlocal`  默认一个线程调度任务，一个线程爬取


进程模式:

mac下可能需要`export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`

* `cronjob runlocal --process`, 一个进程调度，默认一个进程爬取

可以加worker:

* `cronjob runlocal --process --num 2`, 一个进程调度，两个进程爬取
