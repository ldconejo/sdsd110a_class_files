import time
import threading

class ExpensiveResource:
    def __init__(self, resource_id):
        # Simulate expensive initialization
        print(f"💰 Creating expensive resource {resource_id} (this takes time!)")
        time.sleep(2)  # Expensive operation
        self.resource_id = resource_id
        self.data = f"Data for resource {resource_id}"
    
    def get_data(self):
        return self.data
    
    def process(self, input_data):
        return f"Processed {input_data} with {self.resource_id}"

class LazyResourceProxy:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self._resource = None  # Not created yet
        self._lock = threading.Lock()
    
    def _get_resource(self):
        """Lazy initialization with thread safety"""
        if self._resource is None:
            with self._lock:
                if self._resource is None:  # Double-checked locking
                    print(f"🔄 Lazy loading resource {self.resource_id}")
                    self._resource = ExpensiveResource(self.resource_id)
        return self._resource
    
    def get_data(self):
        """Delegate to real resource"""
        return self._get_resource().get_data()
    
    def process(self, input_data):
        """Delegate to real resource"""
        return self._get_resource().process(input_data)
    
if __name__ == "__main__":
    # Usage comparison
    print("=== Without Proxy (Immediate Loading) ===")
    start_time = time.time()
    resources = [ExpensiveResource(i) for i in range(3)]  # All created immediately
    print(f"Creation time: {time.time() - start_time:.2f}s")

    print("\n=== With Proxy (Lazy Loading) ===")
    start_time = time.time()
    proxies = [LazyResourceProxy(i) for i in range(3)]  # Created instantly
    print(f"Creation time: {time.time() - start_time:.2f}s")

    # Resources only created when first accessed
    print("\nAccessing first proxy:")
    print(proxies[0].get_data())  # Now resource 0 is created

    print("\nAccessing third proxy:")
    print(proxies[2].process("test"))  # Now resource 2 is created
    # Resource 1 is never created unless accessed!
