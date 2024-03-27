from bs4 import BeautifulSoup as bs
from collections import OrderedDict
import ast
import os

T_xml = os.getcwd() + r"\VasilisImplementation\dummy_1.xml"
D_xml = os.getcwd() + r"\VasilisImplementation\Dependencies.xml"


def xml2list(file):
    # Get the file as input
    with open(file, 'r') as f:
        data = f.read()
    task_set = bs(data, "xml")
    tasks = task_set.find_all('task')
    return tasks

def dep2list(file):
    # Get the file as input
    with open(file, 'r') as f:
        data = f.read()
    dependencies_set = bs(data, "xml")
    dependencies = dependencies_set.find_all('dependency')
    return dependencies


def convertDep2dict(dependencies):
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
 
def splitTasksPerResource(task_set, dependencies, num_of_resources):
    # For duedate calculation split tasks and their dependencies per resource
    tasks_per_resource = [[] for _ in range(num_of_resources)]
    dependencies_per_resource = [{} for _ in range(num_of_resources)]
    
    for id, task in enumerate(task_set):
        task_resource = task['r']
        tasks_per_resource[int(task_resource)].append(task['id'])
    
    for id, task_id in enumerate(dependencies):
        task = task_set[int(task_id)]
        task_resource = task['r']
        for items in dependencies[task_id]:
            succ_task = task_set[int(items)]
            succ_task_resource = succ_task['r']
            if task_id in dependencies_per_resource[int(succ_task_resource)]:
                dependencies_per_resource[int(succ_task_resource)][task_id].append(succ_task['id'])
            else:
                dependencies_per_resource[int(succ_task_resource)][task_id] = [succ_task['id']]
    
    return tasks_per_resource, dependencies_per_resource 
 

def computeDueDatePerResource(task_set, dependencies, tasks_per_resource, dependencies_per_resource, num_of_resources):

    due_dates = {}

    # Traverse the task set from the sink node to the source node in topological order
    for task in reversed(task_set):    
        # Per every resource 
        temp_due_date = [] 
        for resources in range(num_of_resources):
            # Check if it is not a predeccessor of any task in this resource
            if task["id"] not in dependencies_per_resource[resources].keys():
                # If it isn't but is executed in this resource:
                if task["id"] in tasks_per_resource[resources]:
                    due_dates[task["id"]] = float(task["d"])
            # Else
            else:
                # Get successors on this resource and sort them as needed
                successors = dependencies_per_resource[resources][task["id"]]
                successor_due_dates = [[key, float(due_dates[key])] for key in successors if key in due_dates]
                successor_due_dates_ordered = sorted(successor_due_dates, key=lambda x: x[1], reverse=True)
                # Calculation of the due date per resource
                dd_t = float('inf')
                for succ_idx, succ_due_date in successor_due_dates_ordered:
                    if succ_due_date <= dd_t: dd_t = succ_due_date - float(task_set[int(succ_idx)]["e"])
                    else: dd_t = dd_t - float(task_set[int(succ_idx)]["e"])
                temp_due_date.append(min(dd_t, float(task["d"])))
        # Assign the tightest due date out of all the resources to the task
        if temp_due_date: due_dates[task["id"]] = min(temp_due_date)    
        
    return due_dates


taskset = xml2list(T_xml)
deps = dep2list(D_xml)
dependencies = convertDep2dict(deps)
print(dependencies)
numResources = max([int(task["r"]) for task in taskset]) + 1
tasks_per_resource, dependencies_per_resource = splitTasksPerResource(taskset, dependencies, numResources)
print(tasks_per_resource)
print(dependencies_per_resource)
due_dates = computeDueDatePerResource(taskset, dependencies, tasks_per_resource, dependencies_per_resource, numResources)
print(due_dates)


