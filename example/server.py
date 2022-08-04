import flask,flask_socketio,uuid,threading

server=flask.Flask(__name__)
socketio=flask_socketio.SocketIO(server)

class Room:
    def __init__(self,key):
        self.key=key
        threading.Thread(target=socketio.on(self.key+"/fromClient"),args=(self.receive,)).start()

    def join(self,username):
        print(f"{username} joined the room {self.key}")
        self.send("",f"{username} joined the room")

    def receive(self,data):
        self.send(data["username"],data["message"])

    def send(self,username,message):
        socketio.emit(self.key+"/fromServer",data={"username":username,"message":message})

users,rooms=[],{}

@server.route("/connection")
def connection():
    username=flask.request.form['username']
    if username not in users:
        print(f"Received connection from user {username}")
        return "approved"
    else:return "username unavailable"

@server.route("/joinRoom")
def joinRoom():
    key=flask.request.form["key"]
    username=flask.request.form["username"]
    if key in rooms:
        rooms[key].join(username)
        return "approved"
    else:return "invalid"

@server.route("/createRoom")
def createRoom():
    if len(rooms)>2:return "full"
    key=str(uuid.uuid1())
    rooms[key]=Room(key)
    print(f"Created room {key}")
    return key

if __name__=="__main__":
    socketio.run(server)
