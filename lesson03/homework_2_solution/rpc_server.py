import socket
import json
import threading
import math

class RPCServer:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.methods = {}
        
        # Register built-in methods
        self.register_method('add', self.add)
        self.register_method('subtract', self.subtract)
        self.register_method('multiply', self.multiply)
        self.register_method('divide', self.divide)
        self.register_method('power', self.power)
        self.register_method('square_root', self.square_root)
        self.register_method('modulo', self.modulo)
        
    def register_method(self, name, func):
        """Register a method that can be called remotely"""
        self.methods[name] = func

    # Math operations
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    
    def power(self, a, b):
        return a ** b
    
    def square_root(self, a):
        if a < 0:
            raise ValueError("Cannot take square root of a negative number")
        return math.sqrt(a)
    
    def modulo(self, a, b):
        if b == 0:
            raise ValueError("Modulo by zero")
        return a % b
    
    def handle_client(self, client_socket):
        """Handle RPC requests from a client (JSON-RPC 2.0 format)"""
        try:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    request = json.loads(data.decode('utf-8'))
                    method = request.get("method")
                    params = request.get("params", [])
                    request_id = request.get("id")

                    if method not in self.methods:
                        response = {
                            "jsonrpc": "2.0",
                            "error": f"Method '{method}' not found",
                            "id": request_id
                        }
                    else:
                        try:
                            # Call the method dynamically
                            result = self.methods[method](*params)
                            response = {
                                "jsonrpc": "2.0",
                                "result": result,
                                "id": request_id
                            }
                        except Exception as e:
                            response = {
                                "jsonrpc": "2.0",
                                "error": str(e),
                                "id": request_id
                            }

                except json.JSONDecodeError:
                    response = {
                        "jsonrpc": "2.0",
                        "error": "Invalid JSON format",
                        "id": None
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "error": str(e),
                        "id": None
                    }

                # Send the response back to the client
                client_socket.sendall(json.dumps(response).encode('utf-8'))
        
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
    
    def start(self):
        """Start the RPC server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"JSON-RPC Server listening on {self.host}:{self.port}")
        
        try:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"New connection from {addr}")
                thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                thread.start()
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        finally:
            server_socket.close()

if __name__ == "__main__":
    server = RPCServer()
    server.start()
