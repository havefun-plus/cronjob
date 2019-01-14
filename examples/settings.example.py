# 是否使用代理
ENABLE_PROXY = True

# proxy class
PROXY_CLASS = 'spiders.proxy.IterProxy'

# 爬取失败或者http code错误时候需要重试的次数
RETRY_TIMES = 10

# 针对每个请求的时间限制，不同于requests的timeout
REQUEST_TIMEOUT = 30

# 需要重试的http code
RETRY_HTTP_CODE = [429]

# 是否需要更换user agent
ENABLE_REPLACE_USER_AGENT = True

# 爬虫所在路径
SPIDERS_MODULE = 'spiders'

# redis 配置

REDIS_SETTINGS = dict(
    host='0.0.0.0',
    port=6379,
    db=0,
    password=None,
)

# gevent worker queue size
DEFAULT_WORKER_QUEUE_SIZE = 100

# 每个worker默认生产者的协程数
DEFAULT_PRODUCTER_NUMBER = 2

# 每个worker默认消费者的协程数
DEFAULT_CONSUMER_NUMBER = 8
