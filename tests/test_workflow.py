import gevent
import pytest

from tests.helpers import ensure_redis_clear


@ensure_redis_clear
def test_workflow(mocker, queue, registry):
    from cronjob.tasks import task_queue
    from cronjob.tasks.tasks import ProducerTask
    from cronjob.core.worker import Worker

    def _run(self):
        while True:
            try:
                obj = task_queue.get(timeout=3)
                gevent.spawn(obj.run)
                _run.called_count += 1
                if _run.called_count == 3:
                    break
            except Exception as err:
                pass
            finally:
                gevent.sleep(self.n)

    _run.called_count = 0
    mocker.patch.object(Worker, '_run', new=_run)
    task_queue.put(
        ProducerTask(
            redis_queue=queue,
            task_queue=task_queue,
            registry=registry,
        ))
    worker = Worker()
    worker.start()
    worker.join()
    assert _run.called_count == 3
