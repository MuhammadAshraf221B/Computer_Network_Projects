import socket

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server is running on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024).decode()
    if not data:
        break

    command = data[0]
    text = data[1:]

    if command == 'A':
        result = ''.join(sorted(text, reverse=True))
    elif command == 'C':
        result = ''.join(sorted(text))
    elif command == 'D':
        result = text.upper()
    else:
        result = data

    conn.sendall(result.encode())

conn.close()
