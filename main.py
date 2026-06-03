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
lock = threading.Lock()

def start_new_thread(x,y):
    thread = threading.Thread(target=x,args=y)
    thread.start()

def client_handler(client):
    while True:
        data = client.recv(1024)
        if not data:
            print('Bye')
            lock.release()
            break
        client.send(data[::-1])
    client.close()
   
def main():
    # Server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((hostname, port))
        # Three-way-handshake
        server.listen(5)
        
        while True:
            client, address = server.accept()
            print(f"Connected by {address}")
            lock.acquire()
            start_new_thread(client_handler, (client,))

if __name__ == '__main__':
    main()