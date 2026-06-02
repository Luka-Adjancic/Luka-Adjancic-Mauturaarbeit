import socket

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
print(f'Hostname: {hostname}-2')
print(f'IP: {ip}')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((hostname, 7367))