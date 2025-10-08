import socket

def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 6000))
    s.sendall(b"Hello from client!")
    data = s.recv(1024)
    print("Client got:", data.decode())
    s.close()

if __name__ == "__main__":
    client()