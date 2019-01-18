import os
from importlib import import_module

settings = import_module('cronjob.settings.default_settings')

try:
    custom_settings = import_module(
        os.getenv('CRONJOB_SETTINGS', 'cronjob.settings.default_settings'))
except ModuleNotFoundError:
    pass

for key in dir(custom_settings):
    if key.isupper():
        setattr(settings, key, getattr(custom_settings, key))

LOGGING_SETTINGS = dict(
    version=1,
    formatters={
        'default': {
            '()': 'cronjob.utils.utils.Formatter',
            'format':
            '[{asctime}][{levelname}][{module}][{funcName}]: {message}',
            'style': '{'
        },
        'basecls': {
            '()':
            'cronjob.utils.utils.Formatter',
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
        'cronjob': {
            'handlers': ['stdout'],
            'level': settings.LOG_LEVEL,
        },
        'BaseJob': {
            'handlers': ['basecls'],
            'level': 'DEBUG',
        },
    },
)

setattr(settings, 'LOGGING_SETTINGS', LOGGING_SETTINGS)
