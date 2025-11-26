import threading
import queue
import time
import random
from abc import ABC, abstractmethod

# --------------------------------------------------------
# Command Pattern - Tasks
# --------------------------------------------------------

class Task(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_description(self):
        pass


class EmailTask(Task):
    def __init__(self, recipient, subject):
        self.recipient = recipient
        self.subject = subject

    def execute(self):
        duration = random.uniform(0.4, 1.2)
        print(f"[EmailTask] Sending email to {self.recipient} — {duration:.2f}s")
        time.sleep(duration)

        if random.random() < 0.05:
            raise RuntimeError("SMTP error")

        print(f"[EmailTask] Sent to {self.recipient}")

    def get_description(self):
        return f"EmailTask(to={self.recipient}, subject={self.subject})"


class ImageProcessingTask(Task):
    def __init__(self, image_name, operation):
        self.image_name = image_name
        self.operation = operation

    def execute(self):
        duration = random.uniform(1.0, 2.5)
        print(f"[ImageTask] Processing {self.image_name} — {duration:.2f}s")
        time.sleep(duration)

        if random.random() < 0.08:
            raise RuntimeError("Image op failed")

        print(f"[ImageTask] Done {self.image_name}")

    def get_description(self):
        return f"ImageProcessingTask({self.image_name}, {self.operation})"


class ReportTask(Task):
    def __init__(self, report_name, complexity_level=1):
        self.report_name = report_name
        self.complexity_level = complexity_level

    def execute(self):
        duration = random.uniform(0.6, 1.5) * self.complexity_level
        print(f"[ReportTask] Generating {self.report_name} — {duration:.2f}s")
        time.sleep(duration)
        print(f"[ReportTask] Done {self.report_name}")

    def get_description(self):
        return f"ReportTask({self.report_name}, level={self.complexity_level})"


# --------------------------------------------------------
# Worker
# --------------------------------------------------------

class Worker(threading.Thread):
    def __init__(self, task_queue, worker_id, system):
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.worker_id = worker_id
        self.system = system

    def run(self):
        print(f"[Worker-{self.worker_id}] Start")

        while True:
            task = self.task_queue.get()

            if task is None:
                print(f"[Worker-{self.worker_id}] Shutdown signal")
                self.task_queue.task_done()
                break

            desc = task.get_description()
            print(f"[Worker-{self.worker_id}] Running: {desc}")

            try:
                task.execute()

                # Thread-safe global counter
                with self.system.processed_lock:
                    self.system.processed += 1

            except Exception as e:
                print(f"[Worker-{self.worker_id}] Error: {e}")

            finally:
                self.task_queue.task_done()

        print(f"[Worker-{self.worker_id}] Exit")


# --------------------------------------------------------
# Task Queue System
# --------------------------------------------------------

class TaskQueueSystem:
    def __init__(self, num_workers=3, max_queue_size=50):
        self.task_queue = queue.Queue(maxsize=max_queue_size)
        self.workers = []
        self._submitted = 0

        # Atomic global processed counter
        self.processed = 0
        self.processed_lock = threading.Lock()

        for i in range(num_workers):
            w = Worker(self.task_queue, i + 1, self)
            w.start()
            self.workers.append(w)

        print(f"[System] Started with {num_workers} workers")

    def submit_task(self, task, block=True, timeout=1.0):
        try:
            self.task_queue.put(task, block=block, timeout=timeout)
            self._submitted += 1
            print(f"[System] Submitted: {task.get_description()}")
            return True

        except queue.Full:
            print("[System] Queue full")
            return False

    def get_stats(self):
        return {
            "queue": self.task_queue.qsize(),
            "submitted": self._submitted,
            "processed": self.processed,
        }

    def shutdown(self, wait=True):
        print("[System] Shutdown...")

        for _ in self.workers:
            self.task_queue.put(None)

        if wait:
            for w in self.workers:
                w.join()
            print("[System] All workers stopped")


# --------------------------------------------------------
# Demo
# --------------------------------------------------------

def main():
    random.seed(0)
    system = TaskQueueSystem(num_workers=4, max_queue_size=20)

    tasks = [
        EmailTask("alice@example.com", "Welcome"),
        ImageProcessingTask("photo1.jpg", "resize"),
        EmailTask("bob@example.com", "Invoice"),
        ReportTask("weekly-sales", 2),
        ImageProcessingTask("photo2.png", "thumbnail"),
        EmailTask("carol@example.com", "Reset"),
        ReportTask("monthly-summary", 3),
        ImageProcessingTask("photo3.tif", "denoise"),
        EmailTask("dan@example.com", "Newsletter"),
        ReportTask("ad-hoc", 1),
    ]

    total = len(tasks)
    print(f"[Demo] Waiting for {total} tasks...")

    for t in tasks:
        system.submit_task(t)
        time.sleep(random.uniform(0.05, 0.25))

    try:
        while True:
            stats = system.get_stats()
            print(f"[Stats] queue={stats['queue']} submitted={stats['submitted']} processed={stats['processed']}")

            if stats["processed"] >= total and stats["queue"] == 0:
                break

            time.sleep(0.5)

        system.task_queue.join()
        print("[Demo] All tasks done")

    finally:
        system.shutdown()


if __name__ == "__main__":
    main()
