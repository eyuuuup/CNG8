import socket
import threading
import sys
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 1337))
serversocket.listen(5)
client_names = []


def client_thread(clientsocket):
    while True:
        data = clientsocket.recv(4096)
        if data:
            data_string = data.decode("utf-8")
            data_list = data_string.split()
            
            if data_list[0] == "HELLO-FROM":
                string_bytes = "Hello " +  data_list[1]
        
                clientsocket.sendall(string_bytes.encode("utf-8"))

            elif data_list[0] == "@echo":
                string_bytes = data_list[1].encode("utf-8")
                clientsocket.sendall(string_bytes)
            else:
                default = "nothing here"
                string_bytes = default.encode("utf-8")
                clientsocket.sendall(string_bytes)

            
            print(data_list)
        else:
            break

while True:
    (clientsocket, address) = serversocket.accept()
    t = threading.Thread(target=client_thread, args=(clientsocket,))
    t.daemon = True
    t.start()
    print("Still here")
