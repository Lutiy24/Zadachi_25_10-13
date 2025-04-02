import socket
import os
import shutil
import threading

# Server configuration
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
BUFFER_SIZE = 4096
BACKUP_DIR = 'backup_storage'

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def handle_client(client_socket, address):
    print(f"[+] Connection from {address}")
    
    data = client_socket.recv(BUFFER_SIZE).decode()
    if data.startswith("LIST"):
        file_list = data[5:].split("|")
        client_socket.send(b"ACK")
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            save_path = os.path.join(BACKUP_DIR, file_name)
            with open(save_path, 'wb') as f:
                while True:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
        print("[+] Backup completed")
    elif data.startswith("GET"):
        files = os.listdir(BACKUP_DIR)
        client_socket.send("|".join(files).encode())
        for file_name in files:
            file_path = os.path.join(BACKUP_DIR, file_name)
            with open(file_path, 'rb') as f:
                while chunk := f.read(BUFFER_SIZE):
                    client_socket.send(chunk)
        print("[+] Backup files sent")
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")
    while True:
        client_socket, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    start_server()