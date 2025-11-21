from queue import Queue, Empty
import threading
import time

class ThreadSafeObjectPool:
    def __init__(self, factory, min_size=2, max_size=10):
        self.factory = factory
        self.available = Queue(maxsize=max_size)
        self.in_use = set()
        self.lock = threading.Lock()
        self.max_size = max_size
        
        # Pre-create minimum objects
        for _ in range(min_size):
            obj = self.factory()
            self.available.put(obj)
    
    def acquire(self, timeout=5):
        """Thread-safe object acquisition"""
        try:
            obj = self.available.get(timeout=timeout)
            with self.lock:
                self.in_use.add(obj)
            return obj
        except Empty:
            # Try to create new object if under limit
            with self.lock:
                if len(self.in_use) + self.available.qsize() < self.max_size:
                    obj = self.factory()
                    self.in_use.add(obj)
                    return obj
            raise RuntimeError("Pool exhausted and cannot create more objects")
    
    def release(self, obj):
        """Thread-safe object release"""
        with self.lock:
            if obj in self.in_use:
                self.in_use.remove(obj)
                try:
                    self.available.put_nowait(obj)
                except:
                    # Pool full, object will be garbage collected
                    pass

class SampleResource:
    def __init__(self):
        self.created_at = time.time()
    
    def is_valid(self):
        # Simulate resource validity check
        return (time.time() - self.created_at) < 10

def resource_factory():
    return SampleResource()

def worker(thread_id):
    try:
        resource = pool.acquire()
        print(f"Thread {thread_id} acquired resource created at {resource.created_at}")
        time.sleep(1)  # Simulate work
    finally:
        pool.release(resource)
        print(f"Thread {thread_id} released resource")

if __name__ == "__main__":   
    pool = ThreadSafeObjectPool(resource_factory, min_size=2, max_size=5)

    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()