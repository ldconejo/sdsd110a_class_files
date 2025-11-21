import time
import random

class DatabaseConnection:
    """Simulates an expensive database connection"""
    
    def __init__(self):
        # Simulate expensive connection setup
        print("🔗 Creating new database connection...")
        time.sleep(0.2)  # 200ms to create connection
        self.connection_id = random.randint(1000, 9999)
        self.query_count = 0
    
    def query(self, sql):
        """Execute a database query"""
        self.query_count += 1
        time.sleep(0.01)  # Small query time
        return f"Connection {self.connection_id}: Result for '{sql}'"
    
    def close(self):
        """Close the connection"""
        print(f"❌ Closed connection {self.connection_id}")

class ConnectionPool:
    """Simple connection pool for database connections"""
    
    def __init__(self, max_connections=5):
        self.max_connections = max_connections
        self.available_connections = []  # List of available connections
        self.total_connections = 0       # Total connections created
        
        print(f"📦 Created connection pool (max: {max_connections})")
    
    def get_connection(self):
        """Get a connection from the pool"""
        # 1. Reuse an available connection
        if self.available_connections:
            return self.available_connections.pop()

        # 2. Create a new connection if under limit
        if self.total_connections < self.max_connections:
            conn = DatabaseConnection()
            self.total_connections += 1
            return conn

        # 3. Otherwise, no connections are available
        print("⚠️ No connections available (at max capacity)")
        return None
    
    def return_connection(self, connection):
        """Return a connection to the pool"""
        # Avoid duplicates
        if connection not in self.available_connections:
            self.available_connections.append(connection)
    
    def get_stats(self):
        """Get pool statistics"""
        return {
            "available": len(self.available_connections),
            "total_created": self.total_connections,
            "max_connections": self.max_connections
        }

# Test your implementation
def test_basic_functionality():
    """Test basic pool operations"""
    print("=== Testing Basic Pool Functionality ===")
    
    pool = ConnectionPool(max_connections=3)
    print(f"Initial stats: {pool.get_stats()}")
    
    # Test getting connections
    print("\n📥 Getting connections from pool:")
    conn1 = pool.get_connection()
    conn2 = pool.get_connection()
    
    print(f"Stats after getting 2: {pool.get_stats()}")
    
    # Test using connections
    if conn1:
        result1 = conn1.query("SELECT * FROM users")
        print(f"Query result: {result1}")
    
    # Test returning connections
    print("\n📤 Returning connections to pool:")
    if conn1:
        pool.return_connection(conn1)
    if conn2:
        pool.return_connection(conn2)
    
    print(f"Stats after returning: {pool.get_stats()}")
    
    # Test reusing connections
    print("\n♻️ Testing connection reuse:")
    conn3 = pool.get_connection()  # Should reuse existing connection!
    if conn3:
        result3 = conn3.query("SELECT * FROM products")
        print(f"Reused connection result: {result3}")
        pool.return_connection(conn3)

def test_performance():
    """Compare performance with and without pool"""
    print("\n=== Performance Comparison ===")
    
    # Test without pool (create new connection each time)
    print("🐌 Without pool (creating new connections):")
    start_time = time.time()
    for i in range(5):
        conn = DatabaseConnection()
        result = conn.query(f"SELECT test_{i}")
        conn.close()
    no_pool_time = time.time() - start_time
    print(f"Time without pool: {no_pool_time:.2f} seconds")
    
    # Test with pool (reuse connections)
    print("\n🚀 With pool (reusing connections):")
    pool = ConnectionPool(max_connections=3)
    start_time = time.time()
    for i in range(5):
        conn = pool.get_connection()
        if conn:
            result = conn.query(f"SELECT test_{i}")
            pool.return_connection(conn)
    pool_time = time.time() - start_time
    print(f"Time with pool: {pool_time:.2f} seconds")
    
    # Show improvement
    if no_pool_time > pool_time:
        improvement = ((no_pool_time - pool_time) / no_pool_time) * 100
        print(f"🎉 Pool was {improvement:.1f}% faster!")
    
    print(f"Final pool stats: {pool.get_stats()}")

# Run the tests
if __name__ == "__main__":
    test_basic_functionality()
    test_performance()
