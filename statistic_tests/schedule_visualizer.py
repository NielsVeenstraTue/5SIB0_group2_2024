import matplotlib.pyplot as plt
import numpy as np
import sys

def vizualize(tasks):

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
    ax.set_xticks(np.arange(0, max(task['d'] for task in tasks) + 1, 5))
    ax.grid(True)
    ax.invert_yaxis()  # Invert y-axis to have the cores listed from top to bottom
    #ax.legend()

    plt.show()
