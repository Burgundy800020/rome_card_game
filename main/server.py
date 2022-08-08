import uuid, threading
import flask, flask_socketio
import Game

#initialize flask server and socket units
server = flask.Flask(__name__)
socketIO = flask_socketio.SocketIO(server)

class Room:
    def __init__(self, id):
        self.id = id
        self.isVisible = False #room visibility for players looking for an opponent
        self.clients = []

        #listen for messages from client
        threading.Thread(target=socketIO.on(f"{id}/fromClient"), args=(self.receive, ))

        #initialize game instance
        self.game = Game.GameManager()
    
    def addClient(self, userName, sid):
        #cannot add more than 2 players
        if len(self.clients) < 2:
            self.clients.append(sid)

            #send 2 character choices to player
            self.send({"characters":self.game.generateCharacters}, sid)
        else:
            return
    
    def send(self, data, sid):
        socketIO.emit(f"{self.id}/fromServer", data=data, room=sid)
    
    def receive(self, data):
        pass

#-----------------SERVER-----------------
allRooms = {}
generateID = lambda: str(uuid.uuid1())

@server.route("/")
def default():
    return "<h1>Roman-Card-Game Server</h1>"

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

@server.route("/makeRoomVisible")
def makeRoomVisible():
    #make room visible for users looking for an opponent
    id = flask.request.form["id"]
    allRooms[id].isVisible = True

@socketIO.on("/joinRoom")
def joinRoom(data):
    #add connection to server's room list
    id = flask.request.form["id"]
    userName = flask.request.form["userName"]
    sid = flask.requests.sid
    allRooms[id].addClient(userName, sid)

if __name__ == "__main__":
    socketIO.run(server)
