from cronjob.apps import cron
from cronjob.events import post_action, receiver


@cron(
    rule='1s',
    priority=9,
    cancelled=False,
    right_now=False,
)
def normal_func():
    print('run in normal_func')


@receiver(post_action, normal_func)
def post_normaljob_action(sender):
    print('This will called after `normal_func` called')
