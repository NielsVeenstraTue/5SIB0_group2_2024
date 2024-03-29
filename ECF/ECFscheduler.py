import copy
from bs4 import BeautifulSoup as bs
import ast
from pprint import pprint


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


def ECF(taskset_file, dependencies_file):
    """Read taskset and dependencies, """
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
    return tasks


tasks = ECF('dummy_paper.xml', 'Dependencies_paper.xml')
