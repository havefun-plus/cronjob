import logging

import arrow


class Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        time = arrow.get(record.created)
        return time.isoformat()


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)
