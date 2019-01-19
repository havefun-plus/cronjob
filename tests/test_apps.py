def test_metacls():
    from cronjob.apps import BaseJob

    class ForTestJob(BaseJob):
        rule = '2m'

    assert ForTestJob.interval == 120
    assert ForTestJob.register_key == 'cronjob:registry:ForTestJob'
