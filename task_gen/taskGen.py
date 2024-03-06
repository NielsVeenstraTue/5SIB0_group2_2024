"""Intitial version of task generation/storing"""

from dataclasses import dataclass
from typing import List
import xml.etree.ElementTree as ET

# @dataclass
# class Task:
#     """Save task.
#     Data:
#     ID (int): ID of the task
#     ExecutionTime: Time in ns/ms
#     Deadline: Time in ns/ms
#     Dependency: ID's of tasks that have to finish before starting this one
#     """
#     ID: int
#     ExecutionTime: int
#     Deadline: int
#     Dependency: List[int]

# Tasks = []
# for i in range(4):
#     Tasks.append(Task(i, 5, 5, []))
#
#
# print(Tasks)  # Point(x=1.5, y=2.5, z=0.0)


root = ET.Element('task_set')
task = ET.SubElement(root, 'task', id='1', e='5', d='10', dep='[1,2]')
d = ET.SubElement(task, 'deadline')
d.text = '10'

tree = ET.ElementTree(root)
tree.write('tasks.xml')
