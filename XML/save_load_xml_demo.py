"""Intitial version of task generation/storing"""

from XML_functions import save_xml, load_xml
from data_formats import Task

"""generate, save and load tasks"""
tasks = []
for i in range(4):
    tasks.append(Task(i, i * 2, i * 3, [2,3]))
save_xml(tasks)
loaded_tasks = load_xml('tasks.xml')
print(loaded_tasks == tasks)

