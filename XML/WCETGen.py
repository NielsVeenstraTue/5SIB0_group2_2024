import random
import numpy as np


def constructWCETDistribution(numOfTasks, numOfProcessors, deadline, minWCET, maxWCET, criticals, percentage, taskBudget, critTaskBudget):

    # Non-critical task deadlines
    taskDeadline = deadline * taskBudget
    
    # Generate WCETs based on the Beta Distribution
    alpha = 0.085
    # Arbirtrary mean of distribution based on the number of tasks
    desMean = percentage * (taskDeadline/numOfTasks) * numOfProcessors
    
    # Randomly assign tasks to each processor
    random_draw = list(np.random.randint(numOfProcessors, size=numOfTasks))
    resource_tasks = [random_draw.count(i) for i in range(numOfProcessors)]
    
    # Randomly assign critical tasks to each processor
    if criticals != 0:
        random_draw = list(np.random.randint(numOfProcessors, size=criticals))
        resource_criticals = [random_draw.count(i) for i in range(numOfProcessors)]
    else:
        resource_criticals = [0]*numOfProcessors

    
    # Generate random values within the range [minWCET, maxWCET] for each processor
    total_arrays = []
    total_deadlines = []
    total_resources = []
    for resource in range(numOfProcessors):
        array = (maxWCET - minWCET) * np.random.beta(alpha, alpha*(maxWCET - desMean)/(desMean - minWCET), 
                                                     (resource_tasks[resource]-resource_criticals[resource])) + minWCET
        # Check if total execution time is less than deadline
        array = fixWCET(array, percentage * taskDeadline, minWCET, maxWCET)
        # Deadlines list
        deadlines = [taskDeadline]*(resource_tasks[resource]-resource_criticals[resource])
        # Resource Binding List
        resources = [resource]*(resource_tasks[resource]-resource_criticals[resource])
        
        if criticals != 0:
            # Critical task deadlines
            critTaskDeadline = deadline * critTaskBudget
            # Arbirtrary mean of distribution based on the number of tasks and available processors
            critDesMean = percentage * (critTaskDeadline/numOfTasks) * numOfProcessors
            # Generate random values within the range [minWCET, maxWCET]
            critArray = (maxWCET - minWCET) * np.random.beta(alpha, alpha*(maxWCET - critDesMean)/(critDesMean - minWCET), resource_criticals[resource]) + minWCET
            # Check if total execution time is less than deadline
            critArray = fixWCET(critArray, percentage * critTaskDeadline, minWCET, maxWCET)
            # Deadlines list
            critDeadlines = [critTaskDeadline]*resource_criticals[resource]
            # Resource Binding List
            critResources = [resource]*resource_criticals[resource]
            
            array = np.concatenate((array, critArray), axis=0).tolist()
            deadlines = deadlines + critDeadlines
            resources = resources + critResources
            
        total_arrays += list(array)
        total_deadlines += list(deadlines)
        total_resources += list(resources)
        
    temp = list(zip(total_arrays, total_deadlines, total_resources))
    random.shuffle(temp)
    res1, res2, res3 = zip(*temp)
    # res1 and res2 come out as tuples, and so must be converted to lists.
    array, deadlines, resources = list(res1), list(res2), list(res3)

    return [array, deadlines, resources]


def fixWCET(sequence, deadline, minValue, maxTime):
    # Calculate the current sum of the array
    currentSum = np.sum(sequence)

    # Adjust one of the elements to make the sum equal to the desired sum
    difference = deadline - currentSum
    
    while(difference < 0):
        task_idx = random.randint(0, len(sequence) - 1)
        if sequence[task_idx] < 2*minValue:
            continue
        sequence[task_idx] -= minValue
        difference +=minValue
    
    return sequence
