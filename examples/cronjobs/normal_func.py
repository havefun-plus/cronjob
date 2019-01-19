from cronjob.apps import cron


@cron(rule='1s')
def normal_func():
    print('run in normal_func')
