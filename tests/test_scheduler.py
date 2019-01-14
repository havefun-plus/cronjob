from sspider.core.spiders import BaseSpider
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


def test_scheduler_all(mocker, scheduler):
    from sspider.core.scheduler import Scheduler
    ns = mocker.patch.object(BaseSpider, 'need_schedule', return_value=True)

    def schedule_func(self, spider_cls):
        if spider_cls.need_schedule():
            self.queue.enqueue(spider_cls.registry_key())
            schedule_func.called = True

    schedule_func.called = False
    ForTestSpider.canceled = False
    mocker.patch.object(Scheduler, 'schedule', new=schedule_func)
    scheduler.schedule_all()
    assert ns.called
    assert schedule_func.called
