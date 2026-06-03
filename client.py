import socket

# Variablen
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
port = 7367
print(f'Hostname: {hostname}-2')
print(f'IP: {ip}')
print(f'Port: {port}')
print(f'Write a Message:')
message = input()

# Server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    # Three-way-handshake
    server.connect((hostname, port))
    # b"" konvertiert es zu Bytes
    server.sendall(f"{message}".encode("UTF-8"))
    data = server.recv(1024)

# !r = repr() Rohe Daten
print(f"Received {data.decode("UTF-8")}")