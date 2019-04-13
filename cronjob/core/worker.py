import logging

import gevent
from cronjob.tasks import task_queue
from cronjob.tasks.tasks import ProducerTask
from cronjob.utils.utils import capture_greenlet_exc
from gevent import Greenlet
from gevent.queue import Empty

LOGGER = logging.getLogger(__name__)


class Worker(Greenlet):
    """
    worker会不停干的从task_queue中取task(cronjob.tasks.BaseTask)执行
    """

    def __init__(self, n=0) -> None:
        Greenlet.__init__(self)
        self.n = n

    def _run(self) -> None:
        # 初始化一个task，这个task会不停的从queue里面取任务
        task_queue.put(ProducerTask.from_settings())
        while True:
            try:
                obj = task_queue.get(timeout=3)
                g = gevent.spawn(obj.run)
                g.link_exception(capture_greenlet_exc)
            except Empty:
                pass
            except Exception as err:
                LOGGER.error(f'Worker error', exc_info=True)
            finally:
                gevent.sleep(self.n)

    def close(self) -> None:
        pass
