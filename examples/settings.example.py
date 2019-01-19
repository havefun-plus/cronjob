# ----- general settings -----
# log level

LOG_LEVEL = 'DEBUG'

# 定时任务所在路径
CRONJOBS_MODULE = 'cronjobs'

# redis 配置

REDIS_SETTINGS = dict(
    host='0.0.0.0',
    port=6379,
    db=0,
    password=None,
)

# gevent worker queue size
DEFAULT_TASK_QUEUE_SIZE = 100

# ----- spider job settings -----

# 是否使用代理
ENABLE_PROXY = False

# proxy class
PROXY_CLASS = 'cronjobs.proxy.IterProxy'

# 针对每个请求的时间限制，不同于requests的timeout
REQUEST_TIMEOUT = 30

# 爬取失败或者http code错误时候需要重试的次数
RETRY_TIMES = 10

# 需要重试的http code, 如果开启代理的话，每次重试会换一个代理
RETRY_HTTP_CODE = [429]

# 是否需要更换user agent
ENABLE_REPLACE_USER_AGENT = True
