from tests.helpers import ensure_redis_clear
from tests.spiders.spiders import ForTestSpider


@ensure_redis_clear
def test_periodic(mocker, scheduler, connection):
    def schedule_func(spider_cls):
        spider_cls.canceled = True
        schedule_func.called = True

    schedule_func.called = False

    scheduler.periodic(schedule_func, ForTestSpider)
    assert schedule_func.called
