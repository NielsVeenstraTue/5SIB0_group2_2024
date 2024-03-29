import copy
from bs4 import BeautifulSoup as bs
import ast
from pprint import pprint

FILES = ["dummy_1.xml", "Dependencies.xml"]

class Task:
    def __init__(self, task_id, execution_time, deadline, resource, predecessors=None):
        self.task_id = task_id
        self.execution_time = execution_time
        self.resource = resource
        self.deadline = deadline
        self.predecessors = predecessors if predecessors else []

def convert2Class(taskset, predecessors):
    classSet = []
    for task in taskset:
        if int(task["id"]) in predecessors.keys():
            firstKey = list(predecessors.keys())[0]
            firstVal = list(predecessors[firstKey])
            if firstKey == int(task["id"]):
                # Task ID, Execution Time, Deadline, Resource, Predecessors
                list_of_pred = [int(x) for x in firstVal]
                classSet.append(Task(int(task["id"]), float(task["e"]), float(task["d"]), int(task["r"]), list_of_pred))
                predecessors.pop(list(predecessors)[0])
        else:
            classSet.append(Task(int(task["id"]), float(task["e"]), float(task["d"]), int(task["r"]), ))
    return classSet

def convert_dependencies_to_dict(dependencies)->dict:
    return {'pred': int(dependencies['pred']), 'succ':int(dependencies['succ'])}

def convert_taskset_to_dict(taskset)->dict:
    return {'id':int(taskset['id']), 'e':float(taskset['e']), 'r':int(taskset['r']), 'd':float(taskset['d'])}

def xml2list(file):
    # Get the file as input
    with open(file, 'r') as f:
        data = f.read()
    task_set = bs(data, "xml")
    tasks = task_set.find_all('task')
    task_set = list()
    for t in tasks:
        task_set.append({'id':int(t['id']), 'e':float(t['e']), 'r':int(t['r']), 'd':float(t['d'])})
    return task_set

def dep2list(file):
    # Get the file as input
    with open(file, 'r') as f:
        data = f.read()
    dependencies_set = bs(data, "xml")
    dependencies = dependencies_set.find_all('dependency')
    dependencies_set = list()
    for dep in dependencies:
        dependencies_set.append({'pred': int(dep['pred']), 'succ':int(dep['succ'])})
    return dependencies_set

def convertDep2Succ(dependencies):
    # Convert dependencies xml to working dictionary format
    predecessors = []
    successors = []
    dictionary = {}
    for id, task in enumerate(dependencies):
        predecessors.append(task['pred'])
        successors.append(task['succ'])

    for pred, succ in zip(predecessors, successors):
        if pred in dictionary:
            dictionary[pred].append(succ)
        else:
            dictionary[pred] = [succ]

    for key in dictionary:
        dictionary[key].sort()

    return dictionary

def convertDep2Pred(dependencies):
    # Convert dependencies xml to working dictionary format
    predecessors = []
    successors = []
    dictionary = {}
    for id, task in enumerate(dependencies):
        predecessors.append(task['pred'])
        successors.append(task['succ'])

    for pred, succ in zip(predecessors, successors):
        if succ in dictionary:
            dictionary[succ].append(pred)
        else:
            dictionary[succ] = [pred]

    for key in dictionary:
        dictionary[key].sort()

    return dictionary

def find_directory_by_id(directories, name):
    for directory in directories:
        if directory["id"] == name:
            return directory
    return None


taskset_file = 'dummy_paper.xml'
dependencies_file = 'Dependencies_paper.xml'


# def ECF(taskset_file, dependencies_file):
taskset = xml2list(taskset_file)
numResources = max([int(task["r"]) for task in taskset]) + 1
deps = dep2list(dependencies_file)
# predecessors = convertDep2Pred(deps)
numTasks = len(taskset)

tasks = []
for i in range(numTasks):
    # Store tasks to a format that can be used
    tasks.append(dict(taskset[i].items()))
    tasks[i]['dep'] = []
    # tasks[i]['scheduled'] = 0
    # tasks[i]['tStart'] = 0
    tasks[i]['CALAP'] = tasks[i]['d'] # CALAP = min(CALAP_successor - exec_successor, deadline)


for i in range(len(deps)):
    # add the dependencies, task[i]['dep'] should be done before i can start
    tasks[deps[i]['succ']]['dep'].append(deps[i]['pred'])

for i in range(numTasks-1, 0, -1):
    """Assign CALAP, working backwards. Assigned CALAP is the minimum of the current CALAP (deadline of assigned 
    before) and the potential new CALAP = CALAP_pred - EXEC_pred """
    for pred in tasks[i]['dep']:
        tasks[pred]['CALAP'] = min(tasks[pred]['CALAP'], tasks[i]['CALAP'] - tasks[i]['e'])
        # print(pred)

    # schedule = partitioned_edf_scheduler(taskset, numResources)
    # return schedule



# if __name__ == '__main__':
#     ECF(FILES[0], FILES[1])
