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

def convertDep2dict(dependencies):
    # Convert dependencies xml to working dictionary format
    predecessors = []
    successors = []
    dictionary = {}
    for id, task in enumerate(dependencies):
        predecessors.append(task['pre'])
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
    task_set_per_resource = [[] for _ in range(num_of_resources)]
    dependencies_per_resource = [[] for _ in range(num_of_resources)]
    
    for id, task in enumerate(task_set):
        task_resource = task['r']
        task_set_per_resource[int(task_resource)].append(task)
    
    
    
    
    return task_set_per_resource, dependencies_per_resource 
 
def computeDueDatePerResource(task_set, dependencies, num_of_resources):

    due_dates = [[] for _ in range(num_of_resources)]
    known_successors = [[] for _ in range(num_of_resources)]
    for id, task in enumerate(task_set):

        # Get its binding resource
        task_resource = task['r']
    
    # Get all immediate successors on the same resource
    d_t = task["dl"]
    dd_t = d_t

    return min(dd_t, d_t)


taskset = xml2list(T_xml)
deps = xml2list(D_xml)
dependencies = convertDep2dict(deps)
print(dependencies)


def schedule(file):

    #########################################################
    # Computing due date per resource #######################
    
    wcet = [] # List to hold all the 'e' values of all the tasks. Can be indexed by ID.
    
    for id, task in enumerate(tasks):
        succ = {}
        d_t = task['dl']
        
        for t in tasks:
            dep_str = t['dep']
            dep_list = ast.literal_eval(dep_str) if dep_str != "[]" else []
            
            if len(wcet) < len(tasks):
                wcet.append(float(t['e'])) 
            
            if id in dep_list: 
                succ[t['id']] = t['dl']
        
        succ_ordered = dict(sorted(succ.items(), key=lambda item: item[1], reverse=True))
        #print(succ_ordered)
        
        dd_t = float('inf')
        
        for t_prime_id, dd_t_prime in succ_ordered.items():
            if float(dd_t_prime) <= dd_t:
                dd_t = float(dd_t_prime) - wcet[int(t_prime_id)]
            else:
                dd_t = float(dd_t) - wcet[int(t_prime_id)]
        
        dd_t = min(dd_t, float(d_t))
        #succ_dd_t.append(dd_t)
        task['dd'] = str(dd_t)
        
 
    #######################################################
    # Scheduling ##########################################
    
    ST = []
    ET = tasks
    
    while len(ST) != len(tasks):
        ET = []
    
    
    
    print(tasks)





