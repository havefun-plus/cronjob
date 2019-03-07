import random
import re
from datetime import datetime

from croniter import croniter


class ConstParser:
    def __init__(self, rule: str) -> None:
        self.rule = rule
        self.parsed = None

    def parse_hms(self) -> int:
        flags = [1, 60, 3600]
        rule = self.rule.lower()
        nums = list(map(int, re.split('[hms]', rule)[:-1]))
        result = 0
        for i, pos in enumerate('smh'):
            if pos in rule:
                result += flags[i] * nums.pop()
        return result

    def is_valid(self) -> True:
        try:
            result = self.parse_hms()
            if isinstance(result, int):
                return True
            return False
        except Exception:
            return False

    def get(self):
        if not self.parsed:
            self.parsed = self.parse_hms()
        return self.parsed


class RandomParser:
    def __init__(self, rule: (tuple, list)) -> None:
        self.rule = rule

    def is_valid(self) -> bool:
        return isinstance(self.rule, (tuple, list)) and len(self.rule) == 2

    def get(self):
        return random.randint(*self.rule)


class CronParser:
    def __init__(self, rule: str):
        self.rule = rule

    def is_valid(self) -> bool:
        return croniter.is_valid(self.rule)

    def get(self):
        now = datetime.now()
        next_time = croniter(self.rule, now).get_next(datetime)
        return (next_time - now).seconds


class CronRule:
    def __init__(self, rule: str) -> None:
        for Parser in [RandomParser, CronParser, ConstParser]:
            parser = Parser(rule)
            if parser.is_valid():
                self.parser = parser
                return
        raise ValueError('Cron rule is invalid!')

    @property
    def interval(self) -> int:
        return self.parser.get()
