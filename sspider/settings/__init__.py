import os
from importlib import import_module

settings = import_module('sspider.settings.default_settings')

try:
    custom_settings = import_module(
        os.getenv('SSPIDER_SETTINGS', 'sspider.settings.default_settings'))
except ModuleNotFoundError:
    pass

for key in dir(custom_settings):
    if key.isupper():
        setattr(settings, key, getattr(custom_settings, key))

LOGGING_SETTINGS = dict(
    version=1,
    formatters={
        'default': {
            '()': 'sspider.utils.utils.Formatter',
            'format':
            '[{asctime}][{levelname}][{module}][{funcName}]: {message}',
            'style': '{'
        },
        'basecls': {
            '()':
            'sspider.utils.utils.Formatter',
            'format':
            '[{asctime}][{levelname}][{basecls}][{funcName}]: {message}',
            'style':
            '{'
        }
    },
    handlers={
        'stdout': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
        },
        'basecls': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'basecls',
        },
    },
    loggers={
        'core': {
            'handlers': ['stdout'],
            'level': settings.LOG_LEVEL,
        },
        'scheduler': {
            'handlers': ['stdout'],
            'level': settings.LOG_LEVEL,
        },
        'engine': {
            'handlers': ['stdout'],
            'level': settings.LOG_LEVEL,
        },
        'worker': {
            'handlers': ['stdout'],
            'level': settings.LOG_LEVEL,
        },
        'queue': {
            'handlers': ['stdout'],
            'level': settings.LOG_LEVEL,
        },
        'registry': {
            'handlers': ['stdout'],
            'level': settings.LOG_LEVEL,
        },
        'BaseSpider': {
            'handlers': ['basecls'],
            'level': 'DEBUG',
        },
        'BaseTask': {
            'handlers': ['basecls'],
            'level': settings.LOG_LEVEL,
        },
    },
)

setattr(settings, 'LOGGING_SETTINGS', LOGGING_SETTINGS)
