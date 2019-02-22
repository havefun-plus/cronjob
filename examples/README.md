### 一、配置文件

目前需要在项目根目录`export PYTHONPATH=.`

通过环境变量`CRONJOB_SETTINGS`指定配置文件, 配置见`settings.example.py`, 也可不指定使用默认配置

### 二、定时任务脚本

所有定时任务默认放在工程根目录下的`cronjobs`文件夹, 或者通过配置`CRONJOBS_MODULE`指定

#### 2.1 通用任务举例

1. 使用类

参考`examples/cronjobs/normal.py`

2. 使用装饰器

参考`examples/cronjobs/normal_func.py`

#### 2.2 以定时爬虫脚本举例

参考`examples/cronjobs/baidu.py`

代理配置参考`examples/cronjobs/proxy.py`


### 三、启动

#### 3.1 主从运行

* 启动主节点: `cronjob runmaster`
* 启动从节点: `cronjob runworker`

* 注意主从运行下`queue`不能指定`thread`或者`process`

#### 3.2 单节点运行

默认线程模式：

* `cronjob runlocal`  默认一个线程调度任务，一个线程爬取


进程模式:

mac下可能需要`export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`

* `cronjob runlocal --process`, 一个进程调度，默认一个进程爬取

* 注意此模式下`queue`不能指定`thread`

可以加worker:

* `cronjob runlocal --process --num 2`, 一个进程调度，两个进程爬取
* 注意此模式下`queue`不能指定`process`
