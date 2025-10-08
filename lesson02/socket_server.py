import socket

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 6000))
    s.listen(1)
    print("Server: Waiting for connection...")
    conn, addr = s.accept()
    print("Server: Connected to", addr)

    data = conn.recv(1024)
    print("Server got:", data.decode())

    conn.sendall(b"Hello from server!")
    conn.close()
    s.close()

if __name__ == "__main__":
    server()