import socket, pickle
import threading

def Receivemsg():
    while True:
        data = s.recv(BUFFER_SIZE)
        if data:
            datalist = pickle.loads(data)
            if (datalist["type"] == "join"):
                if(datalist["username"]!=Username):
                    print("<Server> {} have joined this channel.".format(datalist["username"]))
            elif (datalist["type"] == "message"):
                if(datalist["username"]!=Username):
                    print("<{}> {}".format(datalist["username"], datalist["message"]))

TCP_IP = input("Server: ")
#TCP_IP = "127.0.0.1"
Username = ""
TCP_PORT = 25565
BUFFER_SIZE = 10240

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT)) #เชื่อมต่อ
while True:
    Username = input("Username: ")
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
        message = {
            "username" : Username,
            "type": "message",
            "message": message
        }
        s.send(pickle.dumps(message))