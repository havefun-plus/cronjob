from logging.config import dictConfig

from cronjob.settings import settings

dictConfig(settings.LOGGING_SETTINGS)
