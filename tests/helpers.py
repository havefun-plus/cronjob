from functools import wraps

import fakeredis

fake_connection = fakeredis.FakeStrictRedis()


def ensure_redis_clear(func):
    @wraps(func)
    def wrapper(*args, **wrapper):
        result = func(*args, **wrapper)
        fake_connection.flushall()
        return result

    return wrapper
