def test_enqueue(mocker, queue, connection):
    send_msg = 'test_rk'
    queue.enqueue(send_msg)
    msg = queue.recv()
    assert msg == send_msg
    connection.flushall()
