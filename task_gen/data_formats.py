from dataclasses import dataclass, field
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
    ID: int=-1
    ExecutionTime: int=-1
    Deadline: int=-1
    Dependency: List= field(default_factory=lambda: [])

