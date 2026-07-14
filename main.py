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
def client_handler(client, address, client_connections):
    try:
        while True:
            data = client.recv(1024)
            data = data.decode('ascii')
            if not data:
                print(f'Bye {address}')
                break
            
            if data == 'GET_LIST':
                users = [str(x) for x in client_connections.keys()if x != address]
                client.send(f"Connected Users: {','.join(users)}".encode('ascii'))

            elif ':' in data:
                target_address, message = data.split(':', 1)

                found = False
                for conn_address, conn in client_connections.items():
                    if str(conn_address) == target_address:
                        conn.send(f"Message from {address}: {message}".encode('ascii'))
                        found = True
                        break
                if not found:
                    client.send("User not found.".encode('ascii'))

    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        print(f"Bye {address}")
        del client_connections[address]
        client.close()
        #raddr = client.getpeername()
        #print(f'{data}')
        
   
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
            # erstellt eine Liste mit Clienten
            client_connections[address] = client
            print(f"All possible connections: {list(client_connections.keys())}")
            # erstellt für jeden client einen Thread wo parallel arbeitet
            thread = threading.Thread(target=client_handler,args=(client, address, client_connections))
            #thread2 = threading.Thread(target=start_new_connection,args=(client_connections, client))
            thread.start()
            #thread2.start()
            #time.sleep(15)
            #start_new_thread(client_handler, (client,))

if __name__ == '__main__':
    main()