import socket

HOST = "127.0.0.1"   
PORT = 9999         

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"[Notification Server] Listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"[+] Connection from {addr}")

    message = conn.recv(1024).decode()
    print(f"[NOTIFICATION] {message}")

    conn.close()
