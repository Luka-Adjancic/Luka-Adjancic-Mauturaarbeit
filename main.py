import socket
import time
import threading

# Variablen
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
local = '0.0.0.0'
port = 7367
SEND_BUF_SIZE = 4096 
RECV_BUF_SIZE = 4096
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

            type_indicator = data[0]
            if type_indicator == 0x0:
                users = [addr for addr in client_connections.keys() if addr != address]
                print(users)
                user_list = bytes([0x0])
                for user_ip, user_port in users:
                    ip_bytes = socket.inet_aton(user_ip)
                    port_bytes = user_port.to_bytes(2, byteorder="big")
                    user_list += ip_bytes + port_bytes
                client.sendall(user_list)

            elif type_indicator == 0x1:

                target_ip = socket.inet_ntoa(data[1:5])
                target_port = int.from_bytes(data[5:7], byteorder='big')

                target_address = (target_ip, target_port)
                
                found = False
                for conn_address, conn in client_connections.items():
                    if conn_address == target_address:
                        conn.sendall(data)
                        found = True
                        break
                    if not found:
                        client.send("User not found.".encode('ascii'))

            if not data:
                print(f'Bye {address}')
                break
                

    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        print(f"Bye {address}")
        del client_connections[address]
        client.close()
        
   
def main():
    # Server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((ip, port))
        #bufsize = server.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF) 
        #print ("Buffer size [Before]:%d" %bufsize) 
            
        #server.setsockopt(socket.SOL_TCP, 
                    #socket.TCP_NODELAY, 1) 
        #server.setsockopt( 
                    #socket.SOL_SOCKET, 
                    #socket.SO_SNDBUF, 
                    #SEND_BUF_SIZE) 
        #server.setsockopt( 
                    #socket.SOL_SOCKET, 
                    #socket.SO_RCVBUF, 
                    #RECV_BUF_SIZE) 
        #bufsize = server.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF) 
        #print ("Buffer size [After]:%d" %bufsize)

        server.listen(5)
        client_connections = {}
        while True:
            # Three-way-handshake
            client, address = server.accept()
            print(f"Connected by {address}")
            print(client)
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