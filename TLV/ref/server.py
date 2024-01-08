import socket
import threading

def handle_client(c, addr):
    print(addr, "connected.")

    while True:
        data = c.recv(1024)
        if not data:
            break
        print(data)
        c.sendall(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # socket s 与bind(), listen(), accept()有关
    # socket c 与send(), recv()有关
    s.bind(("0.0.0.0", 1234))
    s.listen()

    while True:
        c, addr = s.accept()
        # 每次accept之后即开启新的thread
        t = threading.Thread(target=handle_client, args=(c, addr))
        t.start()