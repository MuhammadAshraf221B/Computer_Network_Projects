import socket

HOST = '127.0.0.1'
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Connected to the server. Type your message or 'exit' to quit.")

while True:
    message = input("Enter message: ")
    if message.lower() == 'exit':
        break

    client_socket.sendall(message.encode())
    data = client_socket.recv(1024).decode()
    print("Server reply:", data)

client_socket.close()
