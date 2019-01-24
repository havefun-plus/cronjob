from tests.cronjobs.spiders import ForTestSpider
from tests.helpers import ensure_redis_clear


@ensure_redis_clear
def test_singleton(mocker):
    from cronjob.core.registry import Registry
    r1 = Registry('tests.cronjobs')
    r2 = Registry('tests.cronjobs')
    assert r1 is r2


@ensure_redis_clear
def test_crud(registry):
    from cronjob.core.registry import Registry
    registry._initialized = False
    registry = Registry('tests.cronjobs')
    test_sp_rk = list(registry._jobs.keys())[0]

    # test exists
    assert test_sp_rk in registry
    assert registry[test_sp_rk] is ForTestSpider
