from cronjob.apps import cron


@cron(
    rule='1s',
    priority=9,
    cancelled=False,
    right_now=False,
)
def normal_func():
    print('run in normal_func')
