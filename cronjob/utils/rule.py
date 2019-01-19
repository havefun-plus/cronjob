import re
from datetime import datetime

from croniter import croniter


class CronRule:
    def __init__(self, rule: str) -> None:
        self.rule = rule
        if not croniter.is_valid(rule):
            self.const_interval = self.parse_hms()
        else:
            self.const_interval = None

    def parse_hms(self) -> int:
        flags = [1, 60, 3600]
        rule = self.rule.lower()
        l = list(map(int, re.split('[hms]', rule)[:-1]))
        result = 0
        for i, pos in enumerate('smh'):
            if pos in rule:
                result += flags[i] * l.pop()
        return result

    @property
    def interval(self) -> int:
        if self.const_interval:
            return self.const_interval
        now = datetime.now()
        next_time = croniter(self.rule, now).get_next(datetime)
        return (next_time - now).seconds
