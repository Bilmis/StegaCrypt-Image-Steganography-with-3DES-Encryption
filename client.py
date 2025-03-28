import socket
import os

HOST = "127.0.0.1"  # Server address
PORT = 12345  # Must match server port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    # Ask user for the file path
    file_path = input("Enter file path to send (or type 'exit' to quit): ").strip()
    
    if file_path.lower() == "exit":
        client_socket.sendall("DONE".encode())  # Signal server to stop receiving
        break

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        print("Error: Invalid file path. Try again.")
        continue

    filename = os.path.basename(file_path)  # Extract filename

    # Send filename first
    client_socket.sendall(filename.encode())

    # Send file data
    with open(file_path, "rb") as file:
        while (data := file.read(1024)):
            client_socket.sendall(data)

    client_socket.sendall(b"EOF")  # Send EOF signal
    print(f"Sent: {file_path}")

client_socket.close()
print("All files sent successfully.")
