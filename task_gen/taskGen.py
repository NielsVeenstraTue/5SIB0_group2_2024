"""Intitial version of task generation/storing"""

from XML_functions import save_xml, load_xml
from data_formats import Task
from random import randint

def generate_tasks(cores: int):
    """Generate random tasks"""
    scheduleLen = 0 #cycles
    maxLen = 100 #cycles
    tasks = []
    i = 0
    while scheduleLen<maxLen*0.9: #fill minimum 90% of schedule
        WCET = randint(1, maxLen-scheduleLen)
        dl = randint(1, maxLen-WCET - scheduleLen) + WCET + scheduleLen
        tasks.append(Task(i, WCET, dl, []))
        i+=1
        scheduleLen+=WCET

        print(tasks[i-1], )
    return tasks


tasks = []
for i in range(4):
    tasks.append(Task(i, i * 2, i * 3, []))

save_xml(tasks)

loaded_tasks = load_xml('tasks.xml')

print(loaded_tasks == tasks)

generate_tasks(1)




