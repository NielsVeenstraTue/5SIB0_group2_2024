import xml.etree.ElementTree as ET
import random
import os

# move current working directory to current script file location
# to ensure the xml file is in the same folder as the python file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

###### configure parameters here
N_tasks = 15 # max total number of tasks
N_Max_Childs = 3 # max number of child tasks a task can have
Max_Depth = 3 # max number of row of tasks that are dependent of each
Min_deadline_time = 50 # minimum deadline number
Max_deadline_time = 100 # maximum deadline time number for random deadline generation
###### end configure

def create_childs (parent, parentnumber, num_childs):
    curr_task_num = parentnumber
    for i in range (num_childs):
        if (curr_task_num < N_tasks-1):
            curr_task_num += 1
            next_task = ET.SubElement(parent, 'task_' + str(curr_task_num), id=str(curr_task_num),
                        e='unknown', d=str(random.randint(Min_deadline_time, Max_deadline_time)), dependencies=str(parentnumber))
            Task_depth = random.randint(0, Max_Depth)
            create_task(next_task, curr_task_num+1, Task_depth)
            curr_task_num += Task_depth
    
    # make sure we have the correct number of tasks by just creating child nodes
    while (curr_task_num < N_tasks):
        curr_task_num += 1
        next_task = ET.SubElement(next_task, 'task_' + str(curr_task_num), id=str(curr_task_num),
                        e='unknown', d=str(random.randint(Min_deadline_time, Max_deadline_time)), dependencies=str(curr_task_num-1))

def create_task (parent, tasknumber, depth):
    if (depth > 0 and tasknumber < N_tasks):
        next_task = ET.SubElement(parent, 'task_' + str(tasknumber), id=str(tasknumber),
                    e='unknown', d=str(random.randint(Min_deadline_time, Max_deadline_time)), dependencies=str(tasknumber-1))
        create_task(next_task, tasknumber+1, depth-1)

# create root node
task_set = ET.Element('task_set' ,type='PYTHON_MODULE' ,version='4')
i = 0
task_0 = ET.SubElement(task_set, 'root_task', id='0' , e='unknown' 
                       , d=str(random.randint(Min_deadline_time, Max_deadline_time)), dependencies='unknown')
# create child nodes
create_childs(task_0, 0, N_Max_Childs)

# save xml tree
xmlTree = ET.ElementTree(task_set)
ET.indent(xmlTree, space="\t", level=0)
xmlTree.write('task_set.xml', encoding="utf-8")