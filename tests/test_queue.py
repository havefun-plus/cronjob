def test_enqueue(mocker, connection):
    from sspider.queue import Queue
    queue = Queue.from_settings()
    send_msg = 'test_rk'
    queue.enqueue(send_msg)
    msg = queue.recv()
    assert msg == send_msg
    connection.flushall()
