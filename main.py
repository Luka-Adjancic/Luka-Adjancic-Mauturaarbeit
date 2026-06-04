import socket
import time
import threading
import textwrap

# Variablen
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
port = 7367
print(f'Hostname: {hostname}')
print(f'IP: {ip}')
print(f'Port: {port}')

#def start_new_thread(x,y):
    #falsch
    
# nimmt Daten eines Senders und schickt sie umgekehrt zurück
def client_handler(client):
    while True:
        data = client.recv(1024)
        if not data:
            raddr = client.getpeername()
            print(f'Bye {raddr}')
            break
        client.sendall(data[::-1])
    client.close()
   
def main():
    # Server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((hostname, port))
        server.listen(5)
        
        while True:
            time.sleep(15)
            # Three-way-handshake
            client, address = server.accept()
            print(f"Connected by {address}")
            # erstellt für jeden client einen Thread wo parallel arbeitet
            thread = threading.Thread(target=client_handler,args=(client,))
            thread.start()
            #start_new_thread(client_handler, (client,))

if __name__ == '__main__':
    main()