# import matplotlib.pyplot as plt
# from matplotlib.patches import FancyArrow
# import random

# # Sample JSON data (replace this with your actual JSON data)
# dummy_json_data = [
#     {"task": "Task 1", "start": 1, "end": 4, "arrival": 1, "deadline": 5},
#     {"task": "Task 2", "start": 2, "end": 7, "arrival": 2, "deadline": 9},
#     {"task": "Task 3", "start": 3, "end": 9, "arrival": 3, "deadline": 12}
# ]

# dummy_input = [{'id': '0', 'e': 1.0, 'r': 0, 'd': 10.0, 's': 0, 'c': 1.0}, {'id': '2', 'e': 2.0, 'r': 1, 'd': 3.0, 's': 1.0, 'c': 3.0}, {'id': '3', 'e': 1.0, 'r': 1, 'd': 4.0, 's': 3.0, 'c': 4.0}, {'id': '4', 'e': 2.0, 'r': 0, 'd': 5.0, 's': 1.0, 'c': 3.0}, {'id': '5', 'e': 1.0, 'r': 1, 'd': 6.0, 's': 4.0, 'c': 5.0}, {'id': '6', 'e': 1.0, 'r': 0, 'd': 6.0, 's': 4.0, 'c': 5.0}, {'id': '1', 'e': 2.0, 'r': 0, 'd': 7.0, 's': 5.0, 'c': 7.0}]


# def visualize_schedule(json_data):
#     # Plotting
#     fig, axes = plt.subplots(nrows=len(json_data), figsize=(10, len(json_data)*2))

#     for i, task_data in enumerate(json_data):
#         task = task_data["task"]
#         start = task_data["start"]
#         end = task_data["end"]
#         duration = end - start
#         arrival = task_data["arrival"]
#         deadline = task_data["deadline"]
        
#         r = random.randint(0, 255)
#         g = random.randint(0, 255)
#         b = random.randint(0, 255)
        
#         ax = axes[i]
#         ax.barh(task, width=duration, left=start, height=0.5, color='#{:02x}{:02x}{:02x}'.format(r, g, b), align='center', alpha=0.5)
        
#         # Arrival arrow
#         ax.annotate('', xy=(arrival, 0), xytext=(arrival, -0.2), arrowprops=dict(facecolor='g', arrowstyle='->'))
        
#         # Deadline arrow
#         ax.annotate('', xy=(deadline, 0), xytext=(deadline, 0.2), arrowprops=dict(facecolor='r', arrowstyle='->'))
        
#         # Adjust axes limits and labels
#         ax.set_xlim(0, max(deadline + 1, start + duration + 1))
#         ax.set_ylim(-0.5, 0.5)
#         ax.set_xlabel('Time')
#         ax.set_yticks([])
#         ax.set_title(f'Task {i+1}')

#     # Beautify the plot
#     plt.tight_layout()
#     plt.show()

# visualize_schedule(dummy_json_data)

import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('./EDDF')
import EDDFscheduler

T_xml = r"C:\Users\vasri\OneDrive - TU Eindhoven\Documents\TUe Courses\First Year\3rd Quartile\Electronic design automation\Project\5SIB0_group2_2024\Tasksets\NXT Motion_0.57" + r"\taskset.xml"
D_xml = r"C:\Users\vasri\OneDrive - TU Eindhoven\Documents\TUe Courses\First Year\3rd Quartile\Electronic design automation\Project\5SIB0_group2_2024\Tasksets\NXT Motion_0.57" + r"\dependencies.xml"

#tasks, _, _, _ = EDDFscheduler.EDDF(T_xml, D_xml)


tasks = [{'id': '0', 'e': 1.0, 'r': 0, 'd': 10.0, 's': 0, 'c': 1.0}, 
         {'id': '2', 'e': 2.0, 'r': 1, 'd': 3.0, 's': 1.0, 'c': 3.0}, 
         {'id': '3', 'e': 1.0, 'r': 1, 'd': 4.0, 's': 3.0, 'c': 4.0}, 
         {'id': '4', 'e': 2.0, 'r': 0, 'd': 5.0, 's': 1.0, 'c': 3.0}, 
         {'id': '5', 'e': 1.0, 'r': 1, 'd': 6.0, 's': 4.0, 'c': 5.0}, 
         {'id': '6', 'e': 1.0, 'r': 0, 'd': 6.0, 's': 4.0, 'c': 5.0}, 
         {'id': '1', 'e': 2.0, 'r': 0, 'd': 7.0, 's': 5.0, 'c': 7.0}]

# Group tasks by core
cores = {}
for task in tasks:
    core = task['r']
    if core not in cores:
        cores[core] = []
    cores[core].append(task)

fig, ax = plt.subplots()
ax.set_title('Gantt Chart')
ax.set_xlabel('Time')
ax.set_ylabel('Core')

# Define a colormap for distinguishing tasks
colors = plt.cm.tab10(np.linspace(0, 1, len(tasks)))

# Create Gantt chart for each core
for core, core_tasks in cores.items():
    y = [core] * len(core_tasks)
    start_times = [task['s'] for task in core_tasks]
    durations = [task['c'] - task['s'] for task in core_tasks]
    task_ids = [task['id'] for task in core_tasks]

    for i, (start, duration, color, task_id) in enumerate(zip(start_times, durations, colors, task_ids)):
        ax.barh(core, duration, left=start, height=0.5, align='center', color=color, label=f'Task {task_id}')
        ax.text(start + duration / 2, core, f'{task_id}', ha='center', va='center', color='white')

ax.set_yticks(list(cores.keys()))
ax.set_yticklabels([f'Core {core}' for core in cores.keys()])
ax.set_xticks(np.arange(0, max(task['d'] for task in tasks) + 1, 1))
ax.grid(True)
ax.invert_yaxis()  # Invert y-axis to have the cores listed from top to bottom
#ax.legend()

plt.show()
