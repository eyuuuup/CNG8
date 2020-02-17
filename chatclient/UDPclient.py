import socket
import threading
import sys
import time

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("localhost", 1337))
    return s

s = connect()

def getData():
    while (True):
        #https://stackoverflow.com/questions/423379/using-global-variables-in-a-function
        global s
        data = s.recv(4096)
        
        data_string = data.decode("utf-8")
        data_list = data_string.split()

        if len(data_list) == 3 and data_list[0] != "WHO-OK":

            #Send 100 if you want to test this, replace acmessage with one of these.
            message1bitFlipped = b"101"
            message2bitFlipped = b"111"
            message3bitFlipped = b"011"
            acmessage = data_list[2].split('{')[0]
            lrcRecieved = data_list[2].split('{')[1]

            print("MESSAGE INTO BYTEARRAY: " + acmessage)
            dataArray = bytearray(acmessage.encode())
            
            #https://en.wikipedia.org/wiki/Checksum
            #https://stackoverflow.com/questions/29569791/incorrect-lrc-value-calculated-from-checksum
            lrc = 0
            for b in dataArray:
                lrc ^= b
            print("checksum of recieved message: " + str(lrc))
            
            print("checsum of ARRIVED sent message: " + str(lrcRecieved))
           
            if (str(lrc) == str(lrcRecieved)):
               print("No odd-bit error, but you might want to check for a double digit error")
            else:
                print("Yeah you have a odd-bit error")
            


        #https://www.w3resource.com/python/python-bytes.php#byte-string
      
        #print("LOOK: " +  data_list[0])
        #print(data_list)

        if not data: 
            print("Socket is closed.")

        elif data_list[0] == "DELIVERY":
            username = data_list[1]
            acmessage = data_list[2].split('{')[0]
            print("[" + username + " -> me] " + acmessage)

        elif data_list[0] == "BUSY":
            print("Server is full, fuck off.\n")

        elif data_list[0] == "IN-USE":
            print("Username already taken, try again\n")
            #https://stackoverflow.com/questions/40519375/what-does-x-is-used-prior-to-global-declaration-mean-python-2
            s = connect()
            login()

        elif data_list[0] == "SEND-OK":
            print("Message sent.\n")

        elif data_list[0] == "WHO-OK":
            print("Users online: ")
            for x in data_list[1:]:
                print(x)
            print("\n")
        elif data_list[0] == "UNKNOWN":
            print("User not online.")

        else: 
            print(data_string)

t = threading.Thread(target=getData, args=())
#https://stackoverflow.com/questions/2564137/how-to-terminate-a-thread-when-main-program-ends
t.daemon = True
t.start()

def sendDataString(string_bytes):
    string_bytes += "\n"
    #https://stackoverflow.com/questions/42612002/python-sockets-error-typeerror-a-bytes-like-object-is-required-not-str-with?noredirect=1&lq=1
    string_bytes = string_bytes.encode("utf-8")
    s.sendall(string_bytes)

def login():
    name = input("Enter your username: ")
    sendDataString("HELLO-FROM " + name)

def sendMessage(messageTBS):
  
    #https://stackoverflow.com/questions/6903557/splitting-on-first-occurrence
    #https://stackoverflow.com/questions/8113782/split-string-on-whitespace-in-python
    messageSplitted = messageTBS.split(None, 1)
   
    username = messageSplitted[0].split('@')[1]
    message = messageSplitted[1]
    print("MESSAGE INTO BYTEARRAY:  " + message)
    byteMessage = message.encode()
    dataArray = bytearray(byteMessage)
 
    lrc = 0
    for b in dataArray:
        lrc ^= b
    print("checksum of message sent: " + str(lrc))

    sendDataString("SEND " + username + " " + message + "{" + str(lrc))
    print("[me -> " + username + "] " + message + "\n")

    
login()
while(True):
    #https://www.pythoncentral.io/pythons-time-sleep-pause-wait-sleep-stop-your-code/
    time.sleep(0.5)
    command = input("Type in your command: \n")
    if command == "!quit":
        s.close()
        #https://stackoverflow.com/questions/14639077/how-to-use-sys-exit-in-python
        sys.exit(0)
    elif command == "!who":
        sendDataString("WHO")
    elif command[0] == '@':
        sendMessage(command)
    else: 
        sendDataString(command)
    time.sleep(0.5)
