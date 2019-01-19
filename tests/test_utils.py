import operator

import pytest

from cronjob.utils.rule import CronRule
from cronjob.utils.user_agents import replace_user_agent


def test_agent():
    headers = {'headers': {}}
    replace_user_agent(headers)
    assert 'user-agent' in headers['headers']


def test_cronrule():
    tests = [
        ('1H2M3S', operator.eq, 3723),
        ('1h2m3s', operator.eq, 3723),
        ('1h2m', operator.eq, 3720),
        ('1h3s', operator.eq, 3603),
        ('2m3s', operator.eq, 123),
        ('*/5 * * * *', operator.gt, 0),
    ]
    for condition, op, result in tests:
        cr = CronRule(condition)
        assert op(cr.interval, result)

    with pytest.raises(ValueError):
        cr = CronRule('test')
        cr.interval
