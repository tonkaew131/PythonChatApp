import socket, pickle
import threading

userlist = []
conlist = []
def on_new_client(conn, addr):
    while True:
        data = conn.recv(BUFFER_SIZE)
        datalist = pickle.loads(data)
        if (datalist["type"]=="join"):
            if(datalist["username"] in userlist):
                conn.send(pickle.dumps({
                    "type": "error"
                }))
            else:
                userlist.append(datalist["username"])
                conn.send(pickle.dumps({
                    "type": "success"
                }))
                sendmsgtoeveryone("join", "join", datalist["username"], conn)
        elif (datalist["type"]=="message"):
            sendmsgtoeveryone(datalist["message"], "message",  datalist["username"], conn)
        elif (datalist["type"]=="exit"):
            sendmsgtoeveryone("", "exit",  datalist["username"], conn)
            conn.close()
        elif (datalist["type"]=="list"):
            conn.send(pickle.dumps({
                    "type": "list",
                    "username": datalist["username"],
                    "list": ", ".join(userlist)
            }))
    conn.close()

def sendmsgtoeveryone(msg, typee, username, itself):
    cacheconlist = conlist
    print(cacheconlist)
    for curcacheconlist in cacheconlist:
        message = {
            "username" : username,
            "type": typee,
            "message": msg
        }
        curcacheconlist.send(pickle.dumps(message))

TCP_IP = input("Your private ip: ")
TCP_PORT = 25565
BUFFER_SIZE = 10240

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP,TCP_PORT))
s.listen(20)

while 1:
    conn, addr = s.accept()
    conlist.append(conn)
    print("Connect from " + str(addr))
    t = threading.Thread(target=on_new_client, args=(conn, addr))
    t.start()
s.close
