import socket

# Variablen
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
port = 7367
print(f'Hostname: {hostname}-2')
print(f'IP: {ip}')
print(f'Port: {port}')
print(f'Write a Message:')
#message = input()

def main():
    # Server-Connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Three-way-handshake
        server.connect((hostname, port))
        #message = "hey"
        while True:
            message = input()
            server.send(message.encode('ascii'))
            data = server.recv(1024)
            print('Received from server:', data.decode('ascii'))

            answer = input('Do you want to continue (y/n): ')
            if answer.lower() != 'y':
                break
        server.close()
        # b"" konvertiert es zu Bytes
        # b zu .encode geändert damit ich input var benutzten kann
        #server.sendall(f"{message}".encode("UTF-8"))
        #data = server.recv(1024)

# !r = repr() Rohe Daten
# r mit .decode benutzt damit es mit dem .encode funktioniert
#print(f"Received {data.decode("UTF-8")}")

if __name__ == '__main__':
    main()