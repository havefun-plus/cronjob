from tests.cronjobs.spiders import ForTestSpider
from tests.helpers import ensure_redis_clear


@ensure_redis_clear
def test_singleton(mocker, connection):
    from cronjob.core.registry import Registry
    r1 = Registry('tests.cronjobs', connection)
    r2 = Registry('tests.cronjobs', connection)
    assert r1 is r2


@ensure_redis_clear
def test_crud(registry, connection):
    from cronjob.core.registry import Registry
    registry._initialized = False
    registry = Registry('tests.cronjobs', connection)
    test_sp_rk = list(registry._jobs.keys())[0]

    # test exists
    assert test_sp_rk in registry
    assert registry[test_sp_rk] is ForTestSpider
    assert not registry.isdeleted(test_sp_rk)

    # test delete
    registry.delete(test_sp_rk)
    assert registry.isdeleted(test_sp_rk)
    assert test_sp_rk not in registry

    # test add
    registry.add(test_sp_rk)
    assert not registry.isdeleted(test_sp_rk)
    assert test_sp_rk in registry
