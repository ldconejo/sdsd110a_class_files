import socket
import os

SOCKET_PATH = "/tmp/ipc_socket"

def server():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.bind(SOCKET_PATH)
    s.listen(1)
    print("Server ready...")
    conn, _ = s.accept()
    
    data = conn.recv(1024)
    print("Server got:", data.decode())
    conn.sendall(b"Hello from server!")
    conn.close()
    s.close()

if __name__ == "__main__":
    server()
