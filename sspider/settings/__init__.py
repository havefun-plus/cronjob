import os
from importlib import import_module

settings = import_module('settings.default_settings')

try:
    custom_settings = import_module(os.getenv('SSPIDER_SETTINGS'))
except ModuleNotFoundError:
    pass

for key in custom_settings:
    if key.isupper():
        setattr(settings, key, getattr(custom_settings, key))
