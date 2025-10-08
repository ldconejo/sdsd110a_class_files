class Task:
    # __slots__ tells Python to not use a dynamic __dict__, saving memory
    # fixed attributes only
    __slots__ = ("data", "result", "status")  # reduces memory overhead

    def __init__(self):
        self.data = None
        self.result = None
        self.status = "pending"

    def reset(self, data):
        self.data = data
        self.result = None
        self.status = "pending"


class TaskPool:
    def __init__(self, size):
        self.pool = [Task() for _ in range(size)]
        self.available = self.pool[:]  # all tasks start available

    def acquire(self):
        if not self.available:
            # Optionally create new or wait
            self.available.append(Task())  
        return self.available.pop()

    def release(self, task):
        task.reset(None)
        self.available.append(task)


def process_tasks_with_pool(task_data_list):
    results = []
    pool = TaskPool(size=len(task_data_list) // 2)  # preallocate half the number of tasks

    for data in task_data_list:
        task = pool.acquire()
        task.reset(data)

        task.result = data * 2
        task.status = "complete"

        results.append(task.result)
        pool.release(task)  # return object to pool instead of letting GC collect

    return results


# -------------------------------------------------------
# Test
task_data = list(range(10000))
results = process_tasks_with_pool(task_data)
