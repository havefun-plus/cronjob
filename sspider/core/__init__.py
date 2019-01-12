from logging.config import dictConfig

from settings import settings

dictConfig(settings.logging_config)
