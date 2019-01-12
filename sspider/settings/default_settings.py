# 是否使用代理
ENABLE_PROXY = False

# proxy class
PROXY_CLASS = 'net.proxy.DefaultProxy'

# 爬取失败或者http code错误时候需要重试的次数
RETRY_TIMES = 10

# 针对每个请求的时间限制，不同于requests的timeout
REQUEST_TIMEOUT = 30

# 需要重试的http code
RETRY_HTTP_CODE = [429]

# 是否需要更换user agent
ENABLE_REPLACE_USER_AGENT = True

LOGGING_SETTINGS = dict(
    version=1,
    formatters={
        'default': {
            '()': 'utils.utils.Formatter',
            'format':
            '[{asctime}][{levelname}][{module}][{funcName}]: {message}',
            'style': '{'
        },
    },
    handlers={
        'stdout': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
        },
    },
    loggers={
        'core': {
            'handlers': ['stdout'],
            'level': 'DEBUG',
        },
    },
)
