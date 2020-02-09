import socket
import threading
import sys
import time

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("18.195.107.195", 5378))
    return s

s = connect()

def getData():
    while (True):
        #https://stackoverflow.com/questions/423379/using-global-variables-in-a-function
        global s
        data = s.recv(4096)
        #https://www.w3resource.com/python/python-bytes.php#byte-string
        data_string = data.decode("utf-8")
        data_list = data_string.split()
        #print("LOOK: " +  data_list[0])
        #print(data_list)

        if not data: 
            print("Socket is closed.")

        elif data_list[0] == "DELIVERY":
            username = data_list[1]
            message = ""
            #https://stackoverflow.com/questions/6148619/start-index-for-iterating-python-list
            for x in data_list[2:]:
                message += x + " "
            print("[" + username + " -> me] " + message)

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

    sendDataString("SEND " + username + " " + message)
    print("[me -> " + username + "] " + message)
    
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
        print("Command not found.")
    time.sleep(0.5)
