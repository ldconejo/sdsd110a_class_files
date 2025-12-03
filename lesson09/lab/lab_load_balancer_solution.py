# load_balancer_lab.py
import random
import time
from typing import List, Optional

class Server:
    """Represents a web server"""
    
    def __init__(self, server_id: int, name: str):
        self.id = server_id
        self.name = name
        self.active_connections = 0
        self.total_requests = 0
        self.is_healthy = True
    
    def handle_request(self):
        """Process a request (simplified)"""
        self.active_connections += 1
        self.total_requests += 1
        
        # Simulate variable processing time
        processing_time = random.uniform(0.1, 0.3)
        time.sleep(processing_time * 0.01)  # Speed up for demo
        
        self.active_connections -= 1
        return f"Processed by {self.name}"
    
    def fail(self):
        """Simulate server failure"""
        self.is_healthy = False
        print(f"{self.name} has failed!")
    
    def recover(self):
        """Restore server to healthy state"""
        self.is_healthy = True
        print(f"{self.name} has recovered!")

class RoundRobinBalancer:
    """Round Robin load balancing - takes turns with each server"""
    
    def __init__(self, servers: List[Server]):
        self.servers = servers
        self.current_index = 0
    
    def select_server(self) -> Optional[Server]:
        """Select next healthy server in round-robin order"""
        
        # HINT: Use self.current_index to track which server is next
        # HINT: Use % len(self.servers) to wrap around to start
        # HINT: Check server.is_healthy before returning
        # HINT: Try all servers before giving up
        
        # YOUR CODE HERE (3-4 lines)
        attempts = 0
        while attempts < len(self.servers):
            server = self.servers[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.servers)
            
            if server.is_healthy:
                return server
            attempts += 1
        
        return None  # No healthy servers

class LeastConnectionsBalancer:
    """Least Connections load balancing - sends requests to least busy server"""
    
    def __init__(self, servers: List[Server]):
        self.servers = servers
    
    def select_server(self) -> Optional[Server]:
        """Select the healthy server with the fewest active connections"""
        
        # HINT: Filter servers to only healthy ones
        # HINT: Use min() function with key parameter
        # HINT: key should be lambda s: s.active_connections
        
        # YOUR CODE HERE (3-4 lines)
        healthy_servers = [s for s in self.servers if s.is_healthy]
        if not healthy_servers:
            return None
        return min(healthy_servers, key=lambda s: s.active_connections)

class LoadBalancerSimulator:
    """Simulates and compares different load balancing algorithms"""
    
    def __init__(self):
        # Create three servers with different names
        self.servers = [
            Server(1, "FastServer"),
            Server(2, "MediumServer"), 
            Server(3, "SlowServer")
        ]
        
        # Create both algorithms
        self.round_robin = RoundRobinBalancer(self.servers)
        self.least_connections = LeastConnectionsBalancer(self.servers)
    
    def simulate_requests(self, algorithm, algorithm_name: str, num_requests: int = 20):
        """Send requests through the load balancer"""
        
        print(f"\nTesting {algorithm_name} with {num_requests} requests:")
        print("-" * 50)
        
        # Reset server stats
        for server in self.servers:
            server.total_requests = 0
            server.active_connections = 0
        
        # Send requests
        for i in range(num_requests):
            server = algorithm.select_server()
            
            if server:
                # Simulate some servers being slower (more active connections)
                if server.name == "SlowServer":
                    server.active_connections += random.randint(0, 2)
                
                result = server.handle_request()
                print(f"Request {i+1:2d}: {result}")
            else:
                print(f"Request {i+1:2d}: No healthy servers available!")
        
        # Show final distribution
        self.show_distribution(algorithm_name)
    
    def show_distribution(self, algorithm_name: str):
        """Show how requests were distributed across servers"""
        
        print(f"\n{algorithm_name} Results:")
        total_requests = sum(server.total_requests for server in self.servers)
        
        for server in self.servers:
            if total_requests > 0:
                percentage = (server.total_requests / total_requests) * 100
                bar_length = int(percentage / 5)  # Scale bar
                bar = "#" * bar_length
                status = "[UP]" if server.is_healthy else "[DOWN]"
                
                print(f"{status} {server.name:12}: {server.total_requests:2d} requests "
                      f"({percentage:4.1f}%) {bar}")
            else:
                print(f"[DOWN] {server.name:12}: 0 requests")
    
    def simulate_failure_scenario(self):
        """Test how algorithms handle server failures"""
        
        print(f"\nFAILURE SCENARIO TEST")
        print("=" * 50)
        
        # Fail the middle server
        self.servers[1].fail()
        
        # Test both algorithms with failure
        self.simulate_requests(self.round_robin, "Round Robin (with failure)", 15)
        self.simulate_requests(self.least_connections, "Least Connections (with failure)", 15)
        
        # Recover the server
        self.servers[1].recover()
    
    def run_comparison(self):
        """Run complete comparison of algorithms"""
        
        print("LOAD BALANCER ALGORITHM COMPARISON")
        print("=" * 60)
        
        # Test normal conditions
        self.simulate_requests(self.round_robin, "Round Robin", 18)
        self.simulate_requests(self.least_connections, "Least Connections", 18)
        
        # Test failure scenario
        self.simulate_failure_scenario()
        
        # Summary
        print(f"\nKEY INSIGHTS:")
        print("- Round Robin distributes requests evenly across healthy servers")
        print("- Least Connections adapts to servers with different processing speeds")  
        print("- Both algorithms handle server failures by skipping failed servers")
        print("- Choice depends on whether your servers have similar performance")

def main():
    """Run the load balancer simulation"""
    
    print("Welcome to the Load Balancer Lab!")
    print("Algorithms implemented; running the simulation.")
    
    # Create and run simulator
    simulator = LoadBalancerSimulator()
    simulator.run_comparison()
    
    print(f"\nLab Complete! Discuss the results with your classmates.")

if __name__ == "__main__":
    main()
