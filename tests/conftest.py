import pytest
import fakeredis


@pytest.fixture(autouse=True)
def connection(mocker):
    conn = fakeredis.FakeStrictRedis()
    mocker.patch('sspider.connection.connection', conn)
    return conn


@pytest.fixture
def registry(connection):
    from sspider.registry import Registry
    registry = Registry('tests.spiders', connection)
    return registry


@pytest.fixture
def queue(connection):
    from sspider.queue import Queue
    queue = Queue.from_settings()
    return queue


@pytest.fixture
def scheduler(registry, queue):
    from sspider.core.scheduler import Scheduler
    scheduler = Scheduler(registry=registry, queue=queue)
    return scheduler
