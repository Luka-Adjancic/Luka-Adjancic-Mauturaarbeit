import socket
import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno
from Cryptodome.Cipher import AES

# Sehr sicherer Schlüssel
key = b'Password12345678'



# Variablen
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
# IP adress damit sich andere im lokalem Netzwerk verbinden können
exip = '192.168.1.104'
port = 7367
print(f'Hostname: {hostname}-2')
print(f'IP: {ip}')
print(f'Port: {port}')
print("'LIST' for Users that are connected and 'adress:message' to chat with a user")

#user_list = []
#notification = ''

#def window():

def construct_message(ip, port, tag, nonce, ciphertext):

    ip = socket.inet_aton(ip)
    port = int(port).to_bytes(2, byteorder='big')

    #erster Byte ist 0x1 als indicator für die Art der Nachricht
    packet = bytes([0x1])
    packet += ip
    packet += port
    packet += tag
    packet += nonce
    packet += ciphertext

    return packet

def cipher_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return tag, nonce, ciphertext
    
def decipher_message(key, tag, nonce, ciphertext):
    try:
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext
    except ValueError:
        print("Key incorrect or message corrupted")
        return None

# Nachricht empfangen
def receive_messages(client_data):
    while True:
        #nonce = client_data.recv(16)
        #tag = client_data.recv(16)
        #ciphertext = client_data.recv(1024)
        #cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        #plaintext = cipher.decrypt(ciphertext)
        try:
            data = client_data.recv(1024)

            if not data:
                break
            #cipher.verify(tag)
            #print("The message is authentic:", plaintext)
            #try:
                #data = plaintext.decode('ascii')
            type_indicator = data[0]

            if type_indicator == 0x1:
                tag = data[7:23]
                nonce = data[23:39]
                ciphertext = data[39:]
                plaintext = decipher_message(key, tag, nonce, ciphertext)
                if plaintext:
                    notification = plaintext.decode('utf-8')
                    chat_box.config(state="normal")
                    chat_box.insert("end", f"Received: {notification}\n")
                    chat_box.config(state="disabled")

            elif type_indicator == 0x0:
                user_list = []
                actual_data = data[1:]
                # immer 6 bytes fuer ein ip und port paar
                for i in range(0, len(actual_data), 6):
                    header = actual_data[i : i + 6]
                    if len(header) < 6:
                        break
                
                    user_ip = socket.inet_ntoa(header[0:4])
                    user_port = int.from_bytes(header[4:6], byteorder="big")
                    user_list.append(f"{user_ip},{user_port}")
                
                combobox["values"] = user_list
                if user_list:
                    combobox.current(0)

            #except ValueError:
                #print("Key incorrect or message corrupted")

        except Exception as e:
            print(f"receive message Error: {e}")
            break

def main():
    # Server-Connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        # Three-way-handshake
        server.connect((ip, port))
        
        # client thread für Verbindungen
        receiver_thread = threading.Thread(target=receive_messages, args=(server,), daemon=True)
        receiver_thread.start()

        #window_thread = threading.Thread(target=window, daemon=True)
        #window_thread.start()

        while True:
            #message = input('Message or "List": ')

            root = tk.Tk()
            root.title("Chat Box")

            global chat_box

            ipLabel = tk.Label(
                root,
                text=f"Connected to {hostname} ({ip}) on port {port}",
            )
            ipLabel.pack(padx=5, pady=5)

            chat_box = tk.Text(
                root,
                height=10,
                width=50,
                state="disabled",
            )
            chat_box.pack(padx=5, pady=5, fill="both", expand=True)
            

            def get_list():
                server.send(bytes([0x0]))
            
            
            button2 = tk.Button(
                root,
                text="Get List",
                command=get_list,
            )
            button2.pack(padx=5, pady=5)

            global combobox
            
            combobox = ttk.Combobox(
                root,
                values=[],
                state="readonly",
            )
            combobox.set("")
            combobox.pack(padx=5, pady=5, fill="x")

            entry = tk.Entry(
                root,
            )
            entry.pack(padx=5, pady=5, side="left", fill="x", expand=True)
            entry.bind("<Return>", lambda event: send())

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
                # message = "(" + combobox.get() + ")" + ": " + entry.get()
                message = entry.get()
                tag, nonce, ciphertext = cipher_message(message, key)
                #portDst = int(combobox.get().split(',')[1])
                ip, port = combobox.get().split(',')
                # data = message.encode('ascii')
                packet = construct_message(ip, port, tag, nonce, ciphertext)
                #server.sendall(bytes(ipDst) + bytes(portDst) + bytes(nonce) + bytes(tag) + bytes(ciphertext))
                server.sendall(packet)
                chat_box.config(state="normal")
                chat_box.insert("end", f"Sent: {message}\n")
                chat_box.config(state="disabled")
                entry.delete(0, 'end')
                root.focus_set()



            button = tk.Button(
                root,
                text="Send",
                command=send,
            )
            button.pack(padx=5, pady=5, side="right")

            def popup():
                popup = askyesno(title="Annoying Popup", message="Are you sure you want to exit?")
                if popup:
                    root.destroy()
                    exit()

                
                
                
            root.protocol("WM_DELETE_WINDOW", popup)
            root.mainloop()








            #if message.lower() == 'list':
                #server.send("GET_LIST".encode('ascii'))
                #button_is_pressed = False
                #return button_is_pressed
            #elif message.lower() == 'exit':
                #break
            #else:
                #server.send(message.encode('ascii'))
                #button_is_pressed = False
                #return button_is_pressed
                
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