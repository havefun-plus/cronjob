def test_job_klass():
    from cronjob.apps import BaseJob
    from cronjob.events import pre_action, receiver

    class ForTestJob(BaseJob):
        rule = '2m'

        def run(self):
            pass

    assert ForTestJob.interval == 120
    assert ForTestJob.register_key == 'ForTestJob'

    event_called = False

    @receiver(pre_action, sender=ForTestJob, test_args='')
    def test_event(sender, **kwargs):
        nonlocal event_called
        event_called = True
        assert 'test_args' in kwargs

    ForTestJob()()

    assert event_called


def test_func_klass(registry):
    from cronjob.apps import cron
    from cronjob.events import pre_action, receiver

    @cron(rule='2m')
    def cron_func_tester():
        pass

    event_called = False

    @receiver(pre_action, sender=cron_func_tester, test_args='')
    def test_event(sender, **kwargs):
        nonlocal event_called
        event_called = True
        assert 'test_args' in kwargs

    cron_func_tester.cronjob_cls()()
    assert event_called
