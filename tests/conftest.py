import fakeredis
import pytest
from tests.helpers import fake_connection


@pytest.fixture(autouse=True)
def connection(mocker):
    mocker.patch('redis.StrictRedis', fakeredis.FakeStrictRedis)
    return fake_connection


@pytest.fixture
def registry():
    from cronjob.core.registry import Registry
    registry = Registry('tests.cronjobs')
    return registry


@pytest.fixture
def queue(connection):
    from cronjob.queues import get_queue_client
    q = get_queue_client(dict(queue_type='redis', config={}))
    q.set_qname('test')
    return q


@pytest.fixture
def scheduler(registry, queue):
    from cronjob.core.scheduler import Scheduler
    scheduler = Scheduler(registry=registry, queue=queue)
    return scheduler
