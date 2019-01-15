import logging
import traceback

import gevent
from gevent import Greenlet
from gevent.queue import Empty

from sspider.settings import settings
from sspider.tasks import task_queue
from sspider.tasks.tasks import ProducerTask

LOGGER = logging.getLogger('worker')


class Worker(Greenlet):
    def __init__(self, n=0):
        Greenlet.__init__(self)
        self.n = n

    def _run(self):
        task_queue.put(ProducerTask.from_settings())
        while True:
            try:
                obj = task_queue.get(timeout=3)
                gevent.spawn(obj.run)
            except Empty:
                pass
            except Exception as err:
                traceback.print_exc()
                LOGGER.error(f'Worker error: {err}')
            finally:
                gevent.sleep(self.n)

    def close(self):
        pass
