def test_singleton(mocker):
    from sspider.registry import Registry
    r1 = Registry.from_settings()
    r2 = Registry.from_settings()
    assert r1 is r2


def test_crud(connection):
    from sspider.registry import Registry
    registry = Registry('tests.spiders', connection)
