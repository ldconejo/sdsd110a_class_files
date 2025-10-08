# Frequent allocation/deallocation
class Task:
    def __init__(self, data):
        self.data = data
        self.result = None
        self.status = "pending"

def process_tasks_bad(task_data_list):
    results = []
    for data in task_data_list:
        # New object for each task
        task = Task(data)
        task.result = data * 2
        task.status = "complete"
        results.append(task.result)
        # Object becomes garbage
    return results

# Process many tasks
task_data = list(range(10000))
results = process_tasks_bad(task_data)
