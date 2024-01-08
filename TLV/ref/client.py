import socket

# client side has only one socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 1234))
    s.sendall(b"Hello, Ross!")
    data = s.recv(1024)
    print("Received: ", repr(data))
