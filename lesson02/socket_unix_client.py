import socket

SOCKET_PATH = "/tmp/ipc_socket"

def client():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(SOCKET_PATH)
    s.sendall(b"Hello from client!")
    data = s.recv(1024)
    print("Client got:", data.decode())
    s.close()

if __name__ == "__main__":
    client()
