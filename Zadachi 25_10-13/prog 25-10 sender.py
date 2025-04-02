# Sender Client
def send_files(server_host, file_paths):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, SERVER_PORT))
    file_list_str = "|".join(file_paths)
    client.send(f"LIST {file_list_str}".encode())
    client.recv(BUFFER_SIZE)
    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            while chunk := f.read(BUFFER_SIZE):
                client.send(chunk)
    client.close()
    print("[+] Files sent for backup")
