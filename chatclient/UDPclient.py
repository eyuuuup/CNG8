import socket
import threading
import sys
import time

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("18.195.107.195", 5382))
    return s

def checksum(data, length):
    sum1 = 0
    sum2 = 0

    for x in range(0, length):
        sum1 = (sum1 + data[x]) % 255
        sum2 = (sum2 + sum1) % 255

    return (sum2 << 8) | sum1

ackReceived = True

def ackTimer(message):
    global ackReceived
    print("ACKTIMER CALLED")
    timer = 0
    while not ackReceived:
        print("ACKTIMER " + str(timer))
        timer += 1
        time.sleep(1)
        if(timer == 50):
            print("CAN'T SEND MESSAGE, BACKING OFF")
            print("FEEL FREE TO TYPE IN ANOTHER COMMAND")
            ackReceived = True
            return
        if(timer % 10 == 0):
            sendMessage(message)
        
    return
    
s = connect()


def getData():
    while (True):
        try:
            global s
            data = s.recv(4096)
            print(data)
            data_string = data.decode("utf-8")
            data_list = data_string.split()

            if data_list[0] == "DELIVERY":
                username = data_list[1]
                message = ""
                for x in data_list[2:]:
                    message += x + " "

                if(message.strip() == "ACK".strip()):
                    global ackReceived
                    ackReceived = True
                    print("ACK RECEIVED")
                else:
                        
                    receivedMessage = message.strip().split("{")
                    actualMessage = receivedMessage[0]
                    print(receivedMessage)
                    dataByteArray = bytearray(actualMessage, encoding="utf-8")

                    dataByteArray.append(int(receivedMessage[1]))
                    dataByteArray.append(int(receivedMessage[2]))
                    csum = checksum(dataByteArray, len(dataByteArray))
                    if csum == 0:
                        print("No error found\n")
                    else:
                        print("Error found\n")

                    print("[" + username + " -> me] " + actualMessage)
                    sendDataString("SEND " + username + " " + "ACK")
                    break

            if not data: 
                print("Socket is closed.")

            elif data_list[0] == "BUSY":
                print("Server is full, fuck off.\n")

            elif data_list[0] == "IN-USE":
                print("Username already taken, try again\n")
                s = connect()
                login()

            elif data_list[0] == "SEND-OK":
                print("Message sent.\n")

            elif data_list[0] == "SET-OK":
                print("SETTING HAS BEEN CHANGED.\n")
            
            elif data_list[0] == "VALUE":
                print(data_list)

            elif data_list[0] == "WHO-OK":
                print("Users online: ")
                for x in data_list[1:]:
                    print(x)
                print("\n")
            elif data_list[0] == "UNKNOWN":
                print("User not online.")

            elif data_list[0] == "HELLO":
                print("SERVER SAYS HELLO " + data_list[1])

            else: 
                username = data_list[1]
                message = ""
                for x in data_list[2:]:
                    message += x + " "

                if(message.strip() == "ACK".strip()):
                    ackReceived = True
                    print("ACK RECEIVED")
                else:
                        
                    receivedMessage = message.strip().split("{")
                    actualMessage = receivedMessage[0]
                    print(receivedMessage)
                    dataByteArray = bytearray(actualMessage, encoding="utf-8")

                    dataByteArray.append(int(receivedMessage[1]))
                    dataByteArray.append(int(receivedMessage[2]))
                    csum = checksum(dataByteArray, len(dataByteArray))
                    
                    if csum == 0:
                        print("No error found\n")
                    else:
                        print("Error found\n")

                    print("[" + username + " -> me] " + actualMessage)
                    sendDataString("SEND " + username + " " + "ACK")
        except:
            print("ERROR DETECTED")

t = threading.Thread(target=getData, args=())
t.daemon = True
t.start()

def sendDataString(string_bytes):
    string_bytes += "\n"
    string_bytes = string_bytes.encode("utf-8")
    s.sendall(string_bytes)

def login():
    name = input("Enter your username: ")
    sendDataString("HELLO-FROM " + name)

def sendMessage(messageTBS):
  
    messageSplitted = messageTBS.split(None, 1)
   
    username = messageSplitted[0].split('@')[1]
    message = messageSplitted[1]
    dataByteArray = bytearray(message, encoding = "utf-8")

    csum = checksum(dataByteArray, len(dataByteArray))
    f0 = csum & 0xff
    f1 = (csum >> 8) & 0xff
    c0 = 0xff - ((f0 + f1) % 0xff)
    c1 = 0xff - ((f0 + c0) % 0xff)
     
    dataByteArray.append(c0)
    dataByteArray.append(c1)

    printMessage = message
    message += "{" + str(c0) + "{" + str(c1)

    sendDataString("SEND " + username + " " + message)
    
    global ackReceived
    ackReceived = False
    print("[me -> " + username + "] " + printMessage + "\n")

login()
while(True):
    time.sleep(0.5)
    command = input("Type in your command: \n")

    if command == "!quit":
        #s.close()
        sys.exit(0)

    elif command == "!who":
        sendDataString("WHO")

    elif command[0] == '@':
        if not (ackReceived):
            print("Waiting for ack...")
        else:
            sendMessage(command)
            t = threading.Thread(target=ackTimer, args=(command, ))
            t.daemon = True
            t.start()

    else: 
        sendDataString(command)
    time.sleep(0.5)
