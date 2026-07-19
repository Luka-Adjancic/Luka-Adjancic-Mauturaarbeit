import socket
import threading
from gui import send

# Variablen
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
# IP adress damit sich andere im lokalem Netzwerk verbinden können
exip = '192.168.1.23'
port = 7367
print(f'Hostname: {hostname}-2')
print(f'IP: {ip}')
print(f'Port: {port}')
print("'LIST' for Users that are connected and 'adress:message' to chat with a user")
#message = input()


# Nachricht empfangen
def receive_messages(client_data):
    while True:
        try:
            data = client_data.recv(1024).decode('ascii')
            if data:
                print(f"\nIncoming {data}\nMessage or 'List': ", end="")
        
        except:
            break

def main():
    # Server-Connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Three-way-handshake
        server.connect((ip, port))
        
        # client thread für Verbindungen
        receiver_thread = threading.Thread(target=receive_messages, args=(server,), daemon=True)
        receiver_thread.start()

        while True:
            
            message = input(send)
            
            if message.lower() == 'list':
                server.send("GET_LIST".encode('ascii'))
            elif message.lower() == 'exit':
                break
            else:
                server.send(message.encode('ascii'))
                
            #request = input('Do you want to connect with users (y/n): ')
            
                #server.sendall(server_message.encode('ascii'))
                #response = server.recv(1024)
                #print(f'Server responded with: {response.decode(ascii)}')
            
                
            #else:
                #break
            #data = server.recv(1024)
            #print('connected to:', data.decode('ascii'))

            #answer = input('Do you want to continue (y/n): ')
            #if answer.lower() != 'y':
                #break
    #server.close()
        # b"" konvertiert es zu Bytes
        # b zu .encode geändert damit ich input var benutzten kann
        #server.sendall(f"{message}".encode("UTF-8"))
        #data = server.recv(1024)

# !r = repr() Rohe Daten
# r mit .decode benutzt damit es mit dem .encode funktioniert
#print(f"Received {data.decode("UTF-8")}")

if __name__ == '__main__':
    main()