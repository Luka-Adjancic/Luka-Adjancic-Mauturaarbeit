import socket
import tkinter
import threading
from tkinter import *
from tkinter import ttk

# Variablen
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
# IP adress damit sich andere im lokalem Netzwerk verbinden können
exip = '192.168.1.23'
port = 7367
print(f'Hostname: {hostname}-2')
print(f'IP: {ip}')
print(f'Port: {port}')
print(f'Write a Message:')
#message = input()

#root = Tk()
#frm = ttk.Frame(root, padding=10, height=700, width=800)
#frm.grid()
#ttk.Label(frm, text="Simple Messenger").grid(column=0, row=0)
#entry = ttk.Entry(frm, ).grid(column=0, row=1)
#ttk.Button(frm, text="Send",).grid(column=1, row=1)
#root.mainloop()

def receive_messages(client_data):
    while True:
        

def main():
    # Server-Connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Three-way-handshake
        server.connect((ip, port))
        
        receiver_thread = threading.Thread()

        while True:
            
            server.sendall(server_message.encode('ascii'))
            #request = input('Do you want to connect with users (y/n): ')
            #if request.lower() == 'y':
                #server.sendall(server_message.encode('ascii'))
                #response = server.recv(1024)
                #print(f'Server responded with: {response.decode(ascii)}')
                #message = input(f'Choose a connection: {connections.decode('ascii')}')
                #server.send(message.encode('ascii'))
            #else:
                #break
            #data = server.recv(1024)
            #print('connected to:', data.decode('ascii'))

            #answer = input('Do you want to continue (y/n): ')
            #if answer.lower() != 'y':
                #break
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