from logging.config import dictConfig

from sspider.settings import settings

dictConfig(settings.LOGGING_SETTINGS)
