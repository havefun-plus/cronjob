import pytest

from tests.helpers import ensure_redis_clear


class CalledEnough(Exception):
    pass


@ensure_redis_clear
def test_workflow(mocker, queue, registry):
    from sspider.tasks import task_queue
    from sspider.tasks.tasks import ProducerTask
    from sspider.core.worker import Worker

    def run(self):
        try:
            obj = task_queue.get(timeout=3)
            obj.run()
            run.called_count += 1
            if run.called_count == 3:
                raise CalledEnough
        except Exception as err:
            raise

    run.called_count = 0
    mocker.patch.object(Worker, '_work', new=run)
    task_queue.put(
        ProducerTask(
            redis_queue=queue,
            task_queue=task_queue,
            registry=registry,
        ))
    with pytest.raises(CalledEnough):
        worker = Worker()
        worker.work()
