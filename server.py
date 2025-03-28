import socket
import os

HOST = "127.0.0.1"  # Localhost (same system)
PORT = 12345  # Listening port
SAVE_FOLDER = "C:\\Users\\USER\\Documents\\ReceivedFiles"  # Change this to your preferred folder

# Ensure the save folder exists
os.makedirs(SAVE_FOLDER, exist_ok=True)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}...")

conn, addr = server_socket.accept()
print(f"Connection established with {addr}")

while True:
    # Receive filename
    filename = conn.recv(1024).decode()
    if filename == "DONE":
        print("All files received. Closing connection.")
        break

    # Create full save path
    save_path = os.path.join(SAVE_FOLDER, os.path.basename(filename))  # Save with original name

    # Receive file data
    with open(save_path, "wb") as file:
        while True:
            data = conn.recv(1024)
            if not data or data == b"EOF":  # EOF signals end of file
                break
            file.write(data)

    print(f"Received: {filename} -> Saved as: {save_path}")

conn.close()
server_socket.close()
