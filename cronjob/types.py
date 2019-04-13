from typing import Generic, TypeVar

JOB_TYPE = TypeVar('JOB_TYPE')
QUEUE_TYPE = TypeVar('QUEUE_TYPE')
BASE_QUEUE = Generic[QUEUE_TYPE]
