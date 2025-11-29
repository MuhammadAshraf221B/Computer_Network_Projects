import socket
import threading
import datetime

client_counter = 0

def handle_client(conn, addr, client_name):
    print(f"{client_name} connected from {addr[0]}:{addr[1]}")

    while True:
        data = conn.recv(1024).decode().strip()

        if not data:
            break

        if data == "QUIT":
            print(f"{client_name} disconnected.")
            conn.close()
            return

        if ":" not in data and data not in ["TIME", "DATE"]:
            response = f"ERROR: Unknown command from {client_name}."
            conn.send(response.encode())
            print(f"{client_name} sent: {data} → {response}")
            continue

        # BONUS: TIME & DATE
        if data == "TIME":
            result = datetime.datetime.now().strftime("%H:%M:%S")
            conn.send(result.encode())
            print(f"{client_name} sent: TIME → {result}")
            continue

        if data == "DATE":
            result = datetime.datetime.now().strftime("%Y-%m-%d")
            conn.send(result.encode())
            print(f"{client_name} sent: DATE → {result}")
            continue

        command, message = data.split(":", 1)
        command = command.strip()
        message = message.strip()

        # Execute commands
        if command == "UPPER":
            result = message.upper()
        elif command == "LOWER":
            result = message.lower()
        elif command == "REVERSE":
            result = message[::-1]
        elif command == "COUNT":
            result = str(len(message))
        # BONUS: VOWELS
        elif command == "VOWELS":
            vowels = "aeiouAEIOU"
            count = sum(1 for ch in message if ch in vowels)
            result = str(count)
        else:
            result = f"ERROR: Unknown command from {client_name}."

        conn.send(result.encode())
        print(f"{client_name} sent: {data} → {result}")


def main():
    global client_counter

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 2210))
    server.listen()

    print("Server is running on port 2210")

    while True:
        conn, addr = server.accept()

        client_counter += 1
        client_name = f"Client{client_counter}"

        thread = threading.Thread(target=handle_client, args=(conn, addr, client_name))
        thread.start()


main()
