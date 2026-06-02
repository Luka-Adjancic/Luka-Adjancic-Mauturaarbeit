import socket

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print(f'Hostname: {hostname}')
print(f'IP: {ip}')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((hostname, 7367))
server.listen()
client, address = server.accept()
