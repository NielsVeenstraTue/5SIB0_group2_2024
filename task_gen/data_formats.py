from dataclasses import dataclass
from typing import List

@dataclass
class Task:
    """Save task.
    Data:
    ID (int): ID of the task
    ExecutionTime: Time in ns/ms
    Deadline: Time in ns/ms
    Dependency: ID's of tasks that have to finish before starting this one
    """
    ID: int
    ExecutionTime: int
    Deadline: int
    Dependency: List[int]

