import socket
import json

class RemoteCalculator:
    """Proxy object that makes remote calls look like local method calls"""
    
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.socket = None
        self.request_id = 0
        self.connect()
    
    def connect(self):
        """Connect to the RPC server"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"Connected to RPC server at {self.host}:{self.port}")
    
    def _remote_call(self, method_name, *args):
        """Internal method to make JSON-RPC calls"""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "method": method_name,
            "params": args,
            "id": self.request_id
        }
        try:
            # Send request
            self.socket.sendall(json.dumps(request).encode('utf-8'))
            
            # Receive response
            response_data = self.socket.recv(4096)
            response = json.loads(response_data.decode('utf-8'))
            
            # Check for errors
            if "error" in response:
                raise Exception(response["error"])
            return response.get("result")
        except Exception as e:
            raise Exception(f"RPC Error calling '{method_name}': {e}")
    
    # Proxy methods that forward calls to the server
    def add(self, a, b):
        return self._remote_call('add', a, b)
    
    def subtract(self, a, b):
        return self._remote_call('subtract', a, b)
    
    def multiply(self, a, b):
        return self._remote_call('multiply', a, b)
    
    def divide(self, a, b):
        return self._remote_call('divide', a, b)
    
    def power(self, a, b):
        return self._remote_call('power', a, b)
    
    def square_root(self, a):
        return self._remote_call('square_root', a)
    
    def modulo(self, a, b):
        return self._remote_call('modulo', a, b)
    
    def close(self):
        """Close connection to server"""
        if self.socket:
            self.socket.close()
            print("Disconnected from server")

def main():
    # Create remote calculator proxy
    calc = RemoteCalculator()
    
    try:
        # Run initial tests
        print("\nTesting RPC Calculator...")
        print(f"5 + 3 = {calc.add(5, 3)}")
        print(f"10 - 4 = {calc.subtract(10, 4)}")
        print(f"6 * 7 = {calc.multiply(6, 7)}")
        print(f"15 / 3 = {calc.divide(15, 3)}")
        print(f"2 ^ 8 = {calc.power(2, 8)}")
        print(f"√49 = {calc.square_root(49)}")
        print(f"20 % 3 = {calc.modulo(20, 3)}")
        
        # Test error handling
        try:
            calc.divide(10, 0)
        except Exception as e:
            print(f"Expected error: {e}")
        
        # Interactive mode
        print("\n--- Interactive Mode ---")
        print("Type 'quit' to exit.")
        print("Examples:")
        print("  add 5 3")
        print("  square_root 16")
        print("  power 2 10")
        print("------------------------")
        
        while True:
            expr = input("> ").strip()
            if expr.lower() == 'quit':
                break
            if not expr:
                continue

            try:
                parts = expr.split()
                method_name = parts[0]
                args = [float(p) if '.' in p else int(p) for p in parts[1:]]
                
                if not hasattr(calc, method_name):
                    print(f"Unknown method '{method_name}'")
                    continue
                
                method = getattr(calc, method_name)
                result = method(*args)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}")
            
    finally:
        calc.close()

if __name__ == "__main__":
    main()
