import socket
import time
import threading

# Variablen
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
port = 7367
print(f'Hostname: {hostname}')
print(f'IP: {ip}')
print(f'Port: {port}')

#def start_new_connection(client_connections, client):
    #client_connections
        
    
# nimmt Daten
def client_handler(client, client_connections):
    while True:
        data = client.recv(1024)
        data = f'{data.decode('ascii')}' + ' Back'
        data = data.encode('ascii')
        raddr = client.getpeername()
        print(f'{data}')
        if not data:
            print(f'Bye {raddr}')
            break

    client.close()
   
def main():
    # Server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((hostname, port))
        server.listen(5)
        client_connections = {}
        while True:
            # Three-way-handshake
            client, address = server.accept()
            print(f"Connected by {address}")
            client_connections[address] = client.getpeername()
            print(f"All possible connections: {client_connections}")
            # erstellt für jeden client einen Thread wo parallel arbeitet
            thread = threading.Thread(target=client_handler,args=(client, client_connections))
            #thread2 = threading.Thread(target=start_new_connection,args=(client_connections, client))
            thread.start()
            #thread2.start()
            time.sleep(15)
            #start_new_thread(client_handler, (client,))

if __name__ == '__main__':
    main()