import logging
import traceback

import gevent
from gevent.queue import Empty

from sspider.settings import settings
from sspider.tasks import task_queue
from sspider.tasks.tasks import ProducerTask

LOGGER = logging.getLogger('worker')


class Worker:
    def _work(self):
        try:
            obj = task_queue.get(timeout=3)
            obj.run()
        except Empty:
            pass
        except Exception as err:
            traceback.print_exc()
            LOGGER.error(f'Worker error: {err}')

    def work(self):
        while True:
            self._work()
            gevent.sleep(1)

    def close(self):
        pass

    def run(self):
        task_queue.put(ProducerTask.from_settings())
        workers = [self.work for _ in range(settings.DEFAULT_WORKER_NUMBER)]
        gevent.joinall([gevent.spawn(worker) for worker in workers])
