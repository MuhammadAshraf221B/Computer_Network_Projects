import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 2210))

print("Connected to server.")

while True:
    msg = input("> ")

    client.send(msg.encode())

    if msg == "QUIT":
        print("Connection closed.")
        client.close()
        break

    data = client.recv(1024).decode()
    print("Response from server:", data)
