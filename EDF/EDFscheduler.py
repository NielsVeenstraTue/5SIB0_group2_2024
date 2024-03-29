import copy
from bs4 import BeautifulSoup as bs
import ast
from pprint import pprint

# FILES = ["./Scheduler/dummy_1.xml", "./Scheduler/Dependencies.xml"]

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

def partitioned_edf_scheduler(taskset, num_processors):
    # Sort tasks by deadline in ascending order
    taskset.sort(key=lambda x: x.deadline)
    taskset_copy = copy.deepcopy(taskset)
    # Initialize schedule
    schedule = [[] for _ in range(num_processors)]

    # Keep track of completed tasks
    completed_tasks = set()
    
    # Iterate through each task
    while len(completed_tasks) < len(taskset):
        for task in taskset_copy:
            # Check if all predecessors of the task are completed
            predecessors_completed = all(predecessor in completed_tasks for predecessor in task.predecessors)
            if task.task_id not in completed_tasks and predecessors_completed:
                # Predecessors finish time
                pred_list = []
                for task_temp in taskset:
                    if task_temp.task_id in task.predecessors: pred_list.append(task_temp)
                if not pred_list:
                    if schedule[task.resource]: finishTime = schedule[task.resource][-1]["stopTime"]
                    else: finishTime = 0
                    if finishTime + task.execution_time <= task.deadline:
                        # Assign task to the earliest time
                        schedule[task.resource].append({"id": task.task_id, "resource": task.resource, "startTime": finishTime, "stopTime": finishTime + task.execution_time})
                        # Mark task as completed
                        completed_tasks.add(task.task_id)
                        taskset_copy.remove(task)
                        break
                    else: return None
                else:   
                    for pred in pred_list:
                        if schedule[task.resource]: sameResourceFinishTime = schedule[task.resource][-1]["stopTime"]
                        else: sameResourceFinishTime = 0
                        for processor in range(num_processors):
                            if pred.resource == processor: 
                                curr_schedule = schedule[processor]
                                lastPredDir = find_directory_by_id(curr_schedule, pred.task_id)
                                tempFinishTime = lastPredDir["stopTime"]
                                finishTime = max(sameResourceFinishTime, tempFinishTime)
                    # Check if the task can be scheduled within the deadline
                    if finishTime + task.execution_time <= task.deadline:
                        # Assign task to the earliest time
                        schedule[task.resource].append({"id": task.task_id, "resource": task.resource, "startTime": finishTime, "stopTime": finishTime + task.execution_time})
                        # Mark task as completed
                        completed_tasks.add(task.task_id)
                        taskset_copy.remove(task)
                        break
                    else: return None
    return schedule

def EDF(taskset_file, dependencies_file):
    taskset = xml2list(taskset_file)
    numResources = max([int(task["r"]) for task in taskset]) + 1
    deps = dep2list(dependencies_file)
    predecessors = convertDep2Pred(deps)
    taskset = convert2Class(taskset, predecessors)
    schedule = partitioned_edf_scheduler(taskset, numResources)
    return schedule

