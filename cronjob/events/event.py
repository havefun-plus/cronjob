import traceback
import logging
import functools
from typing import Callable

from .actions import Action
from cronjob.apps import BaseJob

LOGGER = logging.getLogger(__name__)


class Event(list):
    def __call__(self, *args, **kwargs) -> None:
        for f in self:
            try:
                f(*args, **kwargs)
            except Exception:
                LOGGER.error('event error')
                traceback.print_exc()


class receiver:  # noqa
    def __init__(self, action: Action, sender: BaseJob) -> None:
        self.sender = sender
        self.action = action

    def __call__(self, func) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            actions = getattr(self.sender, self.action.name)
            actions.append(func)

        return wrapper
