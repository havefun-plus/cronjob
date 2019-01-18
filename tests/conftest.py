import pytest

from tests.helpers import fake_connection


@pytest.fixture(autouse=True)
def connection(mocker):
    mocker.patch('cronjob.connection.connection', fake_connection)
    return fake_connection


@pytest.fixture
def registry(connection):
    from cronjob.core.registry import Registry
    registry = Registry('tests.cronjobs', connection)
    return registry


@pytest.fixture
def queue(connection):
    from cronjob.queue import Queue
    queue = Queue.from_settings()
    return queue


@pytest.fixture
def scheduler(registry, queue):
    from cronjob.core.scheduler import Scheduler
    scheduler = Scheduler(registry=registry, queue=queue)
    return scheduler
