import random
import numpy as np


def constructWCETDistribution(numOfTasks, numOfProcessors, deadline, minWCET, maxWCET, meanWCET, criticals, taskBudget, critTaskBudget):
    # Non-critical task deadlines
    taskDeadline = deadline * taskBudget
    
    # Generate WCETs based on the Beta Distribution
    # Alpha parameter chosen arbitrarily so that we at least have total range from min to max WCET
    alpha = 0.085
    # Generate random values within the range [minWCET, maxWCET]
    array = (maxWCET - minWCET) * np.random.beta(alpha, alpha*(maxWCET - meanWCET)/(meanWCET - minWCET), (numOfTasks-criticals)) + minWCET
    # Check if total execution time is less than deadline
    array = fixWCET(array, numOfProcessors, taskDeadline, minWCET, maxWCET)
    # Deadlines list
    deadlines = [taskDeadline]*(numOfTasks-criticals)
    if criticals != 0:
        # Critical task deadlines
        critTaskDeadline = deadline * critTaskBudget
        # Generate random values within the range [minWCET, maxWCET]
        critArray = (maxWCET - minWCET) * np.random.beta(alpha, alpha*(maxWCET - meanWCET)/(meanWCET - minWCET), criticals) + minWCET
        # Check if total execution time is less than deadline
        critArray = fixWCET(critArray, numOfProcessors, critTaskDeadline, minWCET, maxWCET)
        # Deadlines list
        critDeadlines = [critTaskDeadline]*criticals
        
        array = np.concatenate((array, critArray), axis=0).tolist()
        deadlines = deadlines + critDeadlines
        
    temp = list(zip(array, deadlines))
    random.shuffle(temp)
    res1, res2 = zip(*temp)
    # res1 and res2 come out as tuples, and so must be converted to lists.
    array, deadlines = list(res1), list(res2)

    return [array, deadlines]


def fixWCET(sequence, parallelUnits, deadline, minValue, maxTime):
    # Calculate the current sum of the array
    currentSum = np.sum(sequence)

    # Adjust one of the elements to make the sum equal to the desired sum
    difference = parallelUnits * deadline - currentSum
    
    while(difference < 0):
        task_idx = random.randint(0, len(sequence) - 1)
        rand_val = random.uniform(minValue, maxTime)
        if sequence[task_idx] < rand_val + minValue:
            continue
        sequence[task_idx] -= rand_val
        difference +=rand_val
    
    return sequence     


constructWCETDistribution(4500, 2, 2*960, 0.01, 30, 2, 200, 1, 0.5)