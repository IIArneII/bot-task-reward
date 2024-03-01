from enum import Enum


class TaskType(str, Enum):
    base = 'base'


class TaskStatus(str, Enum):
    started = 'started'
    completed = 'completed'
    not_completed = 'not_completed'

