from tests.helpers import ensure_redis_clear


@ensure_redis_clear
def test_enqueue(mocker, queue, connection):
    send_msg = 'test_rk'
    queue.put(send_msg)
    msg = queue.get()
    assert msg == send_msg
