import logging
import traceback
import types
from functools import partial
from typing import Callable

from .actions import Action

LOGGER = logging.getLogger(__name__)


class Event(list):
    def __call__(self) -> None:
        for f in self:
            try:
                f()
            except Exception:
                LOGGER.error('event error')
                traceback.print_exc()


class receiver:  # noqa
    def __init__(self, action: Action, sender: 'BaseJob', **kwargs) -> None:
        if isinstance(sender, types.FunctionType):
            self.sender = sender.cronjob_cls
        else:
            self.sender = sender
        self.action = action
        self.kwargs = kwargs

    def __call__(self, func) -> Callable:
        actions = getattr(self.sender, self.action.name)
        actions.append(partial(func, self.sender, **self.kwargs))
        return func
