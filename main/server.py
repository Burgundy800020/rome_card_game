import uuid, threading
import flask, flask_socketio

#initialize flask server and socket units
server = flask.Flask(__name__)
socketIO = flask_socketio.SocketIO(server)

class Room:
    def __init__(self, id):
        self.id = id
        self.clients = []

        #listen for messages from client
        threading.Thread(target=socketIO.on(f"{id}/fromClient"), args=(self.receive, ))
    
    def addClient(self, sid):
        self.clients.append(sid)
    
    def receive(self, data):
        pass

#-----------------SERVER-----------------
allRooms = {}
generateID = lambda: str(uuid.uuid1())

@server.route("/createRoom")
def createRoom():
    if len(allRooms) >= 10:return "FULL" #no more space for another room

    #generate random string as room number, for example
    #741f8bd1-13a6-11ed-86a8-b05adaee0887
    id = generateID()
    while id in allRooms:
        id = generateID()
    allRooms[id] = Room(id)
    return id

@socketIO.on("joinRoom")
def joinRoom(data):
    id = flask.request.form["id"]
    sid = flask.requests.sid
    allRooms["id"].addClient(sid)

if __name__ == "__main__":
    socketIO.run(server, port=3000)