import logging

import arrow


class Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        time = arrow.get(record.created)
        return time.isoformat()
