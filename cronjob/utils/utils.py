import logging
import sys

import arrow
from cronjob.settings import settings
from cronjob.utils.loaders import load_object

LOGGER = logging.getLogger(__name__)

try:
    global_exception_handler = load_object(settings.GLOBAL_EXCEPTION_HANDLER)
except Exception:
    LOGGER.error('load `global_exception_handler` failed, use default.')
    from cronjob.utils.tools import global_exception_handler



class Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        time = arrow.get(record.created)
        return time.isoformat()


class classproperty(object):
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


def capture_greenlet_exc(greenlet):
    try:
        greenlet.get()
    except Exception:
        global_exception_handler(*sys.exc_info())
