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
