import socket, pickle
import threading

def exit_handler():
    onexit = {
        "username" : Username,
        "type": "exit"
    }
    s.send(pickle.dumps(onexit))
    exit()

def Receivemsg():
    while True:
        data = s.recv(BUFFER_SIZE)
        if data:
            datalist = pickle.loads(data)
            if (datalist["type"] == "list"):
                    print("<Server> {} ".format(datalist["list"]))
            elif (datalist["type"] == "join"):
                if(datalist["username"]!=Username):
                    print("<Server> {} have joined this channel.".format(datalist["username"]))
            elif (datalist["type"] == "message"):
                if(datalist["username"]!=Username):
                    print("<{}> {}".format(datalist["username"], datalist["message"]))
            elif (datalist["type"] == "exit"):
                if(datalist["username"]!=Username):
                    print("<Server> {} have been disconnected.".format(datalist["username"]))
            


TCP_IP = input("Server: ")
#TCP_IP = "127.0.0.1"
Username = ""
TCP_PORT = 25565
BUFFER_SIZE = 10240

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT)) #เชื่อมต่อ
while True:
    Username = input("Username: ")
    if(len(Username)>15):
        print("Your username is too long.")
    else:
        firstjoin = {
            "username" : Username,
            "type": "join"
        }
        s.send(pickle.dumps(firstjoin))
        data = s.recv(BUFFER_SIZE)
        datalist = pickle.loads(data)
        if (datalist["type"]=="error"):
            print("This name is already taken.")
        elif (datalist["type"]=="success"):
            break
t = threading.Thread(target=Receivemsg)
t.start()
while 1:
    message = input()
    if message:
        if (len(message)>299):
            print("Your message is too long. ( Under 100 char )")
        else:
            if (message.startswith("/")):
                if (message == "/exit"): exit_handler()
                elif (message == "/list"):
                    message = {
                        "username" : Username,
                        "type": "list"
                    }
                    s.send(pickle.dumps(message))
            else:
                message = {
                    "username" : Username,
                    "type": "message",
                    "message": message
                }
                s.send(pickle.dumps(message))
