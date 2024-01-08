import socket
import threading
import os

WEBROOT = "/Users/shanjiang/OneDrive/文档/GitHub/personal_website"

def handle_client(c, addr):
    print(addr, "connected.")

    with c:
        request = c.recv(1024)

        # Parse HTTP headers
        headers = request.split(b"\r\n")
        file = headers[0].split()[1].decode()

        # Load file content
        if file == "/":
            file = "/index.html"

        try:
            with open(WEBROOT + file, "rb") as f:
                content = f.read()
            response = b"HTTP/1.0 200 OK\r\n\r\n" + content

        except FileNotFoundError:
            response = b"HTTP/1.0 404 NOT FOUND\r\n\r\nFile not found!"

        # Send HTTP response
        c.sendall(response)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # socket s 与bind(), listen(), accept()有关
    # socket c 与send(), recv()有关
    s.bind(("0.0.0.0", 8333))
    s.listen()

    while True:
        c, addr = s.accept()
        # 每次accept之后即开启新的thread
        t = threading.Thread(target=handle_client, args=(c, addr))
        t.start()