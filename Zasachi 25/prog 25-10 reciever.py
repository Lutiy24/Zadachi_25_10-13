# Receiver Client
def receive_files(server_host, save_dir):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, SERVER_PORT))
    client.send(b"GET")
    files = client.recv(BUFFER_SIZE).decode().split("|")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for file_name in files:
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, 'wb') as f:
            while True:
                bytes_read = client.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
    client.close()
    print("[+] Files received and saved")