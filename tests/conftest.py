import pytest
import fakeredis


@pytest.fixture(autouse=True)
def connection(mocker):
    conn = fakeredis.FakeStrictRedis()
    mocker.patch('sspider.connection.connection', conn)
    return conn
