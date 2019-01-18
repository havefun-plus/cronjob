from redis import StrictRedis

from cronjob.settings import settings

connection = StrictRedis(**settings.REDIS_SETTINGS)
