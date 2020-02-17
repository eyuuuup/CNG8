import socket
import threading
import sys
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 1337))
serversocket.listen(64)
clients = []

class User:
    def __init__(self, clientsocket, address, name):
        self.clientsocket = clientsocket
        self.address = address
        self.name = name

    def print(self):
        print(self.clientsocket)
        print(self.address)
        print(self.name)

def client_thread(clientsocket, address):
    while True:
        try:
            if len(clients) >= 64:
                string_bytes = "BUSY"
                clientsocket.sendall(string_bytes.encode("utf-8"))
                return
            data = clientsocket.recv(4096)
            if data:
                data_string = data.decode("utf-8")
                data_list = data_string.split()
                
                if data_list[0] == "HELLO-FROM":
                    username = data_list[1]
                    for x in clients:
                        if x.name == username:
                            string_bytes = "IN-USE"
                            clientsocket.sendall(string_bytes.encode("utf-8"))
                            clientsocket.close()
                            return

                    client = User(clientsocket, address, data_list[1])
                    clients.append(client)
                    client.print()
                    string_bytes = "HELLO " +  data_list[1]
                    clientsocket.sendall(string_bytes.encode("utf-8"))

                elif data_list[0] == "WHO":
                    string_bytes = "WHO-OK "
                    for x in clients:
                        string_bytes += x.name + " "
                    clientsocket.sendall(string_bytes.encode("utf-8"))
                
                elif data_list[0] == "SEND":
                    username = data_list[1]
                    message = ""
            
                    for x in data_list[2:]:
                        message += x + " "

                    online = False
                    for x in clients:
                        if x.name == username:
                            deliver = x
                            messageac = "DELIVERY " + username + " " + message
                            deliver.clientsocket.sendall(messageac.encode("utf-8"))
                            string_bytes = "SEND-OK"
                            clientsocket.sendall(string_bytes.encode("utf-8"))
                            online = True
        
                    if not online:
                        string_bytes = "UNKNOWN"
                        clientsocket.sendall(string_bytes.encode("utf-8"))
                    else:
                      string_bytes = "BAD-RQST-HDR"
                      clientsocket.sendall(string_bytes.encode("utf-8"))
            else:
                for x in clients:
                    if x.clientsocket == clientsocket:
                        clients.remove(x)
                        clientsocket.close()
                        return
        except OSError as msg:
            print(msg)
            for x in clients:
                if x.clientsocket == clientsocket:
                    clients.remove(x)
            break

while True:
    (clientsocket, address) = serversocket.accept()
    t = threading.Thread(target=client_thread, args=(clientsocket, address, ))
    t.daemon = True
    t.start()
    print("Still here")
