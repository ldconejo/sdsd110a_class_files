import threading
from queue import Queue, Empty
import time

class DatabaseConnection:
    def __init__(self, connection_string):
        # Simulate expensive connection setup
        time.sleep(0.1)  # 100ms connection time
        self.connection_string = connection_string
        self.created_at = time.time()
        print(f"🔗 Created new database connection")
    
    def query(self, sql):
        return f"Result for: {sql}"
    
    def is_valid(self):
        # Connections expire after 5 minutes
        return time.time() - self.created_at < 300

class DatabaseConnectionPool:
    def __init__(self, connection_string, min_size=2, max_size=10):
        self.connection_string = connection_string
        self.min_size = min_size
        self.max_size = max_size
        self.pool = Queue(maxsize=max_size)
        self.created_count = 0
        self.lock = threading.Lock()
        
        # Pre-create minimum connections
        for _ in range(min_size):
            self._create_connection()
    
    def _create_connection(self):
        """Create a new connection (called with lock held)"""
        if self.created_count < self.max_size:
            conn = DatabaseConnection(self.connection_string)
            self.pool.put(conn)
            self.created_count += 1
            return conn
        return None
    
    def get_connection(self, timeout=5):
        """Get a connection from the pool"""
        try:
            # Try to get existing connection
            conn = self.pool.get(timeout=timeout)
            
            # Check if connection is still valid
            if conn.is_valid():
                return conn
            else:
                # Connection expired, create new one
                with self.lock:
                    self.created_count -= 1
                    return self._create_connection()
        
        except Empty:
            # Pool is empty, try to create new connection
            with self.lock:
                return self._create_connection()
    
    def return_connection(self, connection):
        """Return a connection to the pool"""
        if connection and connection.is_valid():
            try:
                self.pool.put_nowait(connection)
            except:
                # Pool is full, connection will be garbage collected
                with self.lock:
                    self.created_count -= 1
    
    def get_pool_stats(self):
        return {
            "pool_size": self.pool.qsize(),
            "created_count": self.created_count,
            "max_size": self.max_size
        }

# Usage with pool
pool = DatabaseConnectionPool("postgres://localhost/mydb")

def process_data_efficiently(data):
    connection = pool.get_connection()
    try:
        result = connection.query(f"SELECT * FROM table WHERE id = {data}")
        return result
    finally:
        pool.return_connection(connection)

# Now 1000 calls reuse connections!
if __name__ == "__main__":
    large_dataset = range(1000)
    for item in large_dataset:
        process_data_efficiently(item)
