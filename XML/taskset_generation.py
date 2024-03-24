"""Initial version of all taskset generations"""

from XML_functions import save_xml, load_xml
from data_formats import Task
from dependenceGen import constructTaskDependencyDistribution
from WCETGen import constructWCETDistribution
import random
import numpy as np

# Set seed for reproducability
random.seed(0)
np.random.seed(0)

# For the example of NXT Motion
num_tasks = 4301
num_dependences = 4095
min_dependence = 0
max_dependence = 22
array = constructTaskDependencyDistribution(num_tasks, num_dependences, min_dependence, max_dependence)

print(f"First {max_dependence} values of the array: {array[:max_dependence]}")
print("Sum of the array:", sum(array))
print("Max of the array:", max(array))
print("Min of the array:", min(array))
print("Occurences in array:", [array.count(i) for i in range(max(array)+1)])