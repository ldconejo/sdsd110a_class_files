from abc import ABC, abstractmethod

# Base service interface
class DataService(ABC):
    @abstractmethod
    def get_data(self, key):
        pass

# Simple implementation
class DatabaseService(DataService):
    def __init__(self):
        self.data = {"user1": "John", "user2": "Jane", "user3": "Bob"}
    
    def get_data(self, key):
        return self.data.get(key, "Not found")

# Base decorator
class ServiceDecorator(DataService):
    def __init__(self, service: DataService):
        self._service = service
    
    def get_data(self, key):
        return self._service.get_data(key)

# Logging decorator
class LoggingDecorator(ServiceDecorator):
    def __init__(self, service: DataService):
        self._service = service
    def get_data(self, key):
        print(f"LOG: Requesting data for key: {key}")
        result = self._service.get_data(key)
        print(f"LOG: Returned: {result}")
        return result

# Caching decorator
class CachingDecorator(ServiceDecorator):
    def __init__(self, service: DataService):
        super().__init__(service)
        self.cache = {}
    
    def get_data(self, key):
        if key in self.cache:
            print(f"CACHE: Cache hit for {key}")
            return self.cache[key]
        
        print(f"CACHE: Cache miss for {key}")
        result = self._service.get_data(key)
        self.cache[key] = result
        return result

# Performance monitoring decorator
class PerformanceDecorator(ServiceDecorator):
    def get_data(self, key):
        import time
        start_time = time.time()
        result = self._service.get_data(key)
        end_time = time.time()
        print(f"PERF: Request took {(end_time - start_time)*1000:.2f}ms")
        return result

if __name__ == "__main__":
    # Chain multiple decorators
    service = DatabaseService()
    service = LoggingDecorator(service)      # Add logging  
    service = CachingDecorator(service)      # Add caching
    service = PerformanceDecorator(service)  # Add performance monitoring


    # Each request now has caching, logging, and performance monitoring
    print(service.get_data("user1"))  # Cache miss, logged, timed
    print(service.get_data("user1"))  # Cache hit, logged, timed
