"""Intitial version of task generation/storing"""

from XML_functions import save_xml, load_xml
from data_formats import Task
from random import randint

def add_rondom_dependency(tasks, nr_tasks):
    random_set = set()
    for _ in range(randint(1, nr_tasks-1)):
        random_set.add(randint(1, 5))
    print(random_set)


def generate_tasks(nr_tasks: int, cores: int = 0):
    """Generate random tasks"""
    schedule_len = 0  # cycles
    max_len = 100  # cycles
    tasks = []
    # i = 0
    for i in range(nr_tasks):
        WCET = randint(1, round((max_len - schedule_len)/2))
        dl = randint(WCET, max_len)
        tasks.append(Task(i, WCET, dl, []))
        schedule_len += WCET

        print(tasks[i], schedule_len)

    return tasks

"""generate, save and load tasks"""
tasks = []
for i in range(4):
    tasks.append(Task(i, i * 2, i * 3, []))
save_xml(tasks)
loaded_tasks = load_xml('tasks.xml')
print(loaded_tasks == tasks)

"""generate random tasks"""
generate_tasks(5)
