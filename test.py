import socket
from Cryptodome.Cipher import AES

#client side
def construct_message(ip, port, tag, nonce, ciphertext):

    ip = socket.inet_aton(ip)
    port = port.to_bytes(2, byteorder='big')

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


tag, nonce, ciphertext = cipher_message("Hello, World!", b'Sixteen byte key')

print(construct_message('192.168.0.1', 8080, tag, nonce, ciphertext))


def decipher_message(key, tag, nonce, ciphertext):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        return plaintext
    except ValueError:
        print("Key incorrect or message corrupted")
    

def receive_messages(client_data):
    while True:
        data = client_data.recv(1024)
        #nonce = client_data.recv(16)
        #tag = client_data.recv(16)
        #ciphertext = client_data.recv(1024)
        #cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        #plaintext = cipher.decrypt(ciphertext)
        try:
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
                notification = plaintext.decode('utf-8')
                chat_box.config(state="normal")
                chat_box.insert("end", f"Received: {notification}\n")
                chat_box.config(state="disabled")

            elif data:
                user_list = []
                # immer 6 bytes fuer ein ip und port paar
                for i in range(0, len(data), 6):
                    header = data[i : i + 6]
                    if len(header) < 6:
                        break
                
                    user_ip = socket.inet_ntoa(header[0:4])
                    user_port = int.from_bytes(header[4:6], byteorder="big")
                
                    user_list.append(f"{user_ip},{user_port}")
                
                combobox["values"] = user_list

            #except ValueError:
                #print("Key incorrect or message corrupted")

        except:
            break





#server side

def client_handler(client, address, client_connections):
    try:
        while True:
            data = client.recv(1024)

            type_indicator = data[0]
            if type_indicator == 0x0:
                users = [addr for addr in client_connections.keys() if addr != address]
                print(users)
                user_list = b""
                for user_ip, user_port in users:
                    ip_bytes = socket.inet_aton(user_ip)
                    port_bytes = user_port.to_bytes(2, byteorder="big")
                    user_list += ip_bytes + port_bytes
                client.sendall(user_list)

            elif type_indicator == 0x1:
                target_address = socket.inet_ntoa(data[1:5]) + ":" + int.from_bytes(data[5:7], byteorder='big')
                
                found = False
                for conn_address, conn in client_connections.items():
                    if str(conn_address) == target_address:
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