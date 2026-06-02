import socket

# Variablen
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
port = 7367
print(f'Hostname: {hostname}')
print(f'IP: {ip}')
print(f'Port: {port}')

# Server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((hostname, port))
    # Three-way-handshake
    server.listen()
    client, address = server.accept()
    with client:
        print(f"Connected by {address}")
        while True:
            data = client.recv(1024)
            if not data:
                break
            # schickt es zurück
            client.sendall(data)