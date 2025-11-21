from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import threading

class CustomThreadPool:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.work_queue = queue.Queue()
        self.workers = []
        self.shutdown_event = threading.Event()
        
        # Create worker threads
        for i in range(max_workers):
            worker = threading.Thread(target=self._worker_loop, args=(i,))
            worker.daemon = True
            self.workers.append(worker)
            worker.start()
    
    def _worker_loop(self, worker_id):
        """Main loop for worker threads"""
        while not self.shutdown_event.is_set():
            try:
                # Get task from queue
                task_func, args, kwargs, future = self.work_queue.get(timeout=1)
                
                try:
                    # Execute task
                    result = task_func(*args, **kwargs)
                    future.set_result(result)
                except Exception as e:
                    future.set_exception(e)
                finally:
                    self.work_queue.task_done()
                    
            except queue.Empty:
                continue
    
    def submit(self, func, *args, **kwargs):
        """Submit a task to the thread pool"""
        from concurrent.futures import Future
        
        future = Future()
        self.work_queue.put((func, args, kwargs, future))
        return future
    
    def shutdown(self, wait=True):
        """Shutdown the thread pool"""
        self.shutdown_event.set()
        if wait:
            for worker in self.workers:
                worker.join()

# Modern Python approach using ThreadPoolExecutor
def demonstrate_thread_pool():
    def cpu_intensive_task(task_id):
        """Simulate CPU-intensive work"""
        result = sum(i * i for i in range(10000))
        return f"Task {task_id} result: {result}"
    
    print("🧵 Thread Pool Demonstration")
    
    # Using ThreadPoolExecutor (recommended)
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks
        futures = []
        for i in range(10):
            future = executor.submit(cpu_intensive_task, i)
            futures.append(future)
        
        # Collect results
        for future in as_completed(futures):
            result = future.result()
            print(f"✅ {result}")

if __name__ == "__main__":
    demonstrate_thread_pool()