import threading
import queue
import time
import random
from abc import ABC, abstractmethod

# Command Pattern - Tasks as objects
class Task(ABC):
    """Base class for all tasks"""
    
    @abstractmethod
    def execute(self):
        """Execute the task"""
        pass
    
    @abstractmethod
    def get_description(self):
        """Get task description"""
        pass

# TODO: Implement concrete task types
class EmailTask(Task):
    def __init__(self, recipient, subject):
        self.recipient = recipient
        self.subject = subject
    
    def execute(self):
        # TODO: Implement email sending simulation
        pass
    
    def get_description(self):
        # TODO: Return task description
        pass

class ImageProcessingTask(Task):
    def __init__(self, image_name, operation):
        self.image_name = image_name
        self.operation = operation
    
    def execute(self):
        # TODO: Implement image processing simulation
        pass
    
    def get_description(self):
        # TODO: Return task description
        pass

# Worker Thread
class Worker(threading.Thread):
    def __init__(self, task_queue, worker_id):
        super().__init__()
        self.task_queue = task_queue
        self.worker_id = worker_id
        self.processed_count = 0
        self.daemon = True  # Die when main program exits
    
    def run(self):
        # TODO: Implement worker main loop
        # 1. Get tasks from queue
        # 2. Execute tasks
        # 3. Handle shutdown gracefully
        pass

# Main Task Queue System
class TaskQueueSystem:
    def __init__(self, num_workers=3, max_queue_size=10):
        # TODO: Initialize the system
        # 1. Create task queue
        # 2. Create and start worker threads
        # 3. Track system state
        pass
    
    def submit_task(self, task):
        """Submit a task to the queue"""
        # TODO: Add task to queue with error handling
        pass
    
    def get_stats(self):
        """Get system statistics"""
        # TODO: Return queue size, worker info, etc.
        pass
    
    def shutdown(self):
        """Gracefully shutdown the system"""
        # TODO: Stop workers and cleanup
        pass

# Testing and demonstration
def main():
    """Demonstrate the task queue system"""
    # TODO: Create system and submit various tasks
    # TODO: Show that tasks are processed by different workers
    # TODO: Display statistics
    pass

if __name__ == "__main__":
    main()
