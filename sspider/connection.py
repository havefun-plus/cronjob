from redis import StrictRedis

from sspider.settings import settings

connection = StrictRedis(**settings.REDIS_SETTINGS)
