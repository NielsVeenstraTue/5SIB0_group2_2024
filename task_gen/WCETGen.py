import random
import numpy as np

# Set seed for reproducability
random.seed(0)
np.random.seed(0)


def constructWCETDistribution(numOfTasks, numOfProcessors, deadline, minWCET, maxWCET):

    # Generate WCETs based on the Beta Distribution
    # Alpha parameter chosen arbitrarily so that we at least have total range from min to max WCET
    alpha = 0.085
    # Arbirtrary mean of distribution based on the number of tasks and available processors
    desMean = (deadline/numOfTasks) * numOfProcessors
    # Generate random values within the range [minWCET, maxWCET]
    array = (maxWCET - minWCET) * np.random.beta(alpha, alpha*(maxWCET - desMean)/(desMean - minWCET), numOfTasks) + minWCET

    # Check if total execution time is less than deadline
    array = fixWCET(array, numOfProcessors, deadline, minWCET, maxWCET)
    
    return array


def fixWCET(sequence, parallelUnits, maxTime, minValue, maxValue):
    # Calculate the current sum of the array
    currentSum = np.sum(sequence)

    # Adjust one of the elements to make the sum equal to the desired sum
    difference = parallelUnits * maxTime - currentSum

    while(difference < 0):
        task_idx = random.randint(0, len(sequence) - 1)
        if sequence[task_idx] < 2*minValue:
            continue
        sequence[task_idx] -= minValue
        difference +=minValue
    
    return sequence     


# For the example of NXT Motion
num_tasks = 4301
num_processors = 11
max_time = 7.2e-5
min_WCET = 1e-8
max_WCET = 2.25e-6
array = constructWCETDistribution(num_tasks, num_processors, max_time, min_WCET, max_WCET)

print("Sum of the array:", np.sum(array))
print("Average time per core of the array:", np.sum(array)/num_processors)
print("Max of the array:", np.max(array))
print("Min of the array:", np.min(array))
