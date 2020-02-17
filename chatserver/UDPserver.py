import socket
import threading
import sys
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 1337

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
clients = []

class User:
    def __init__(self, address, name):
        self.address = address
        self.name = name

    def print(self):
        print(self.address)
        print(self.name)

def client_thread(data, address):
        try:
            if data:
                data_string = data.decode("utf-8")
                data_list = data_string.split()
                
                if data_list[0] == "HELLO-FROM":
                    username = data_list[1]
                    client = User(address, data_list[1])
                    clients.append(client)
                    string_bytes = "HELLO " +  data_list[1]
                    sock.sendto(string_bytes.encode("utf-8"), address)

                elif data_list[0] == "WHO":
                    string_bytes = "WHO-OK "
                    for x in clients:
                        string_bytes += x.name + " "
                    sock.sendto(string_bytes.encode("utf-8"), address)
                
                elif data_list[0] == "SEND":
                    username = data_list[1]
                    message = ""
            
                    for x in data_list[2:]:
                        message += x + " "

                    online = False
                    for x in clients:
                        if x.name == username:
                            messageac = "DELIVERY " + username + " " + message
                            sock.sendto(messageac.encode("utf-8"), address)
                            string_bytes = "SEND-OK"
                            sock.sendto(string_bytes.encode("utf-8"),address)
                            online = True
        
                    if not online:
                        string_bytes = "UNKNOWN"
                        sock.sendto(string_bytes.encode("utf-8"),address)
                else:
                      string_bytes = "BAD-RQST-HDR"
                      sock.sendto(string_bytes.encode("utf-8"),address)
        except OSError as msg:
            print(msg)

while True:
    data, address = sock.recvfrom(1024)
    client_thread(data, address)
    print("Still here: " + data.decode("utf-8"))
