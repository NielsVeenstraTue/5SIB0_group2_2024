"""Intitial version of task generation/storing"""

from dataclasses import dataclass
from typing import List
from XML_functions import save_XML, load_XML
import xml.etree.ElementTree as ET
from data_formats import Task
import numpy as np


tasks = []
for i in range(4):
    tasks.append(Task(i, i*2, i*3, []))

# print(tasks)
# print(len(tasks))

save_XML(tasks)

loaded_tasks = load_XML('tasks.xml')
# print(loaded_tasks)


print(loaded_tasks==tasks)
