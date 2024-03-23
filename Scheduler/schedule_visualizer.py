import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
import random

# Sample JSON data (replace this with your actual JSON data)
dummy_json_data = [
    {"task": "Task 1", "start_day": 1, "duration": 4, "arrival": 1, "deadline": 5},
    {"task": "Task 2", "start_day": 2, "duration": 7, "arrival": 2, "deadline": 9},
    {"task": "Task 3", "start_day": 3, "duration": 9, "arrival": 3, "deadline": 12}
]


def visualize_schedule(json_data):
    # Plotting
    fig, axes = plt.subplots(nrows=len(json_data), figsize=(10, len(json_data)*2))

    for i, task_data in enumerate(json_data):
        task = task_data["task"]
        start_day = task_data["start_day"]
        duration = task_data["duration"]
        arrival = task_data["arrival"]
        deadline = task_data["deadline"]
        
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        
        ax = axes[i]
        ax.barh(task, width=duration, left=start_day, height=0.5, color='#{:02x}{:02x}{:02x}'.format(r, g, b), align='center', alpha=0.5)
        
        # Arrival arrow
        ax.annotate('', xy=(arrival, 0), xytext=(arrival, -0.2), arrowprops=dict(facecolor='g', arrowstyle='->'))
        
        # Deadline arrow
        ax.annotate('', xy=(deadline, 0), xytext=(deadline, 0.2), arrowprops=dict(facecolor='r', arrowstyle='->'))
        
        # Adjust axes limits and labels
        ax.set_xlim(0, max(deadline + 1, start_day + duration + 1))
        ax.set_ylim(-0.5, 0.5)
        ax.set_xlabel('Day')
        ax.set_yticks([])
        ax.set_title(f'Task {i+1}')

    # Beautify the plot
    plt.tight_layout()
    plt.show()

