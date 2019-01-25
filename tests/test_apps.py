def test_metacls():
    from cronjob.apps import BaseJob
    from cronjob.events.event import receiver
    from cronjob.events.actions import pre_action

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
