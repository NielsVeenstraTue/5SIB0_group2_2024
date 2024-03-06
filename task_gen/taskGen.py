"""Intitial version of task generation/storing"""

from dataclasses import dataclass
from typing import List
from save_XML import save_XML
import xml.etree.ElementTree as ET
from data_formats import Task


tasks = []
for i in range(4):
    tasks.append(Task(i, 5, 5, [2,3]))

# print(tasks)
# print(len(tasks))

save_XML(tasks)
