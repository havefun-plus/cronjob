import logging
import types
from functools import partial
from typing import Any, Callable, List

from .actions import Action

LOGGER = logging.getLogger(__name__)


class Event(list):
    def __init__(self, name, parents):
        super().__init__()
        self.name = name
        self.partents = parents

    def __call__(self) -> None:
        actions: List['Event'] = []
        for item in self.partents:
            more = getattr(item, self.name)
            if more:
                actions.extend(more)
        actions.extend(self)
        for f in actions:
            try:
                f()
            except Exception:
                LOGGER.error('event error', exc_info=True)


class receiver:  # noqa
    def __init__(self, action: Action, sender: Any, **kwargs) -> None:
        if isinstance(sender, types.FunctionType):
            self.sender = sender.cronjob_cls  # type: ignore
        else:
            self.sender = sender
        self.action = action
        self.kwargs = kwargs

    def __call__(self, func) -> Callable:
        actions = getattr(self.sender, self.action.name)
        actions.append(partial(func, self.sender, **self.kwargs))
        return func
