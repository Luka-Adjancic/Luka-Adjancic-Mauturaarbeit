import socket
import threading
import tkinter as tk
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
print("'LIST' for Users that are connected and 'adress:message' to chat with a user")
message = ''
button_is_pressed = False

def window():
    root = tk.Tk()
    root.title("Chat Box")

    def get_list():
        button_is_pressed
        button_is_pressed = True
        message
        message = 'list'
        return message, button_is_pressed
    
    
    button2 = tk.Button(
        root,
        text="Get List",
        command=get_list,
    )
    button2.pack(padx=5, pady=5)

    combobox = ttk.Combobox(root, values=[1, 2, 3, 4, 5])
    combobox.set("")
    combobox.pack(padx=5, pady=5, fill="x")

    entry = tk.Entry(root)
    entry.pack(padx=5, pady=5, fill="x")

    def erase(event=None):
        if entry.get() == 'Type here...':
            entry.delete(0,'end')
    def add(event=None):
        if entry.get() == '':
            entry.insert(0, 'Type here...')

    add()
    entry.bind("<FocusIn>", erase)
    entry.bind("<FocusOut>", add)

    def send():
        send = combobox.get() + ": " + entry.get()
        print(send)
    button = tk.Button(
        root,
        text="Send",
        command=send,
    )
    button.pack(padx=5, pady=5)

    root.mainloop()


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

        window_thread = threading.Thread(target=window, daemon=True)
        window_thread.start()

        while True:

            while button_is_pressed == True:
                
                #message = input('Message or "List": ')
                
                if message.lower() == 'list':
                    server.send("GET_LIST".encode('ascii'))
                    button_is_pressed = False
                    return button_is_pressed
                elif message.lower() == 'exit':
                    break
                else:
                    server.send(message.encode('ascii'))
                    button_is_pressed = False
                    return button_is_pressed
                
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