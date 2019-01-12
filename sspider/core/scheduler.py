from sspider.registry import Registry


class Scheduler:
    key = 'ssspider:scheduler:'

    def __init__(self, *args, **kwargs):
        self.registry = Registry()
