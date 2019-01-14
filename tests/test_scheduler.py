from tests.spiders.spiders import ForTestSpider
from sspider.core.spiders import BaseSpider


def test_periodic(mocker, scheduler, connection):
    def schedule_func(spider_cls):
        spider_cls.canceled = True
        schedule_func.called = True

    schedule_func.called = False

    scheduler.periodic(schedule_func, ForTestSpider)
    assert schedule_func.called
    connection.flushall()


def test_scheduler_all(mocker):
    pass
