import uuid, threading
import flask, flask_socketio
import Game

#initialize flask server and socket units websocket
#server deployed to -> https://roman-card-game.herokuapp.com/
server = flask.Flask(__name__)
socketIO = flask_socketio.SocketIO(server)

class Room:
    def __init__(self, id, public=False, _eventCallback=None):
        self.id = id
        self.public = public #room visibility for players looking for an opponent
        self._eventCallback = _eventCallback #internal variable
        self.clients = []

        
        #listen for messages from client
        threading.Thread(target=socketIO.on(f"{id}/drawCard"), args=(self.drawCard, )).start()

        #initialize game instance
        self.game = Game.GameManager()
    
    def addClient(self, userName, sid):
        #cannot add more than 2 players
        if len(self.clients) < 2:
            self.clients.append(sid)
        else:
            return "FULL" #return FULL if 2 people are already connected

        #send 2 character choices to each player
        if len(self.clients) == 2:
            for sid in self.clients:
                self.send("getCharacterChoices", {"characters":self.game.generateCharacters()}, sid)
        return ""

    def send(self, route, data, sid):
        socketIO.emit(f"{self.id}/{route}", data=data, room=sid)
    
    def drawCard(self, data):
        n = data["n"]

#-----------------SERVER-----------------
allRooms = {}
generateID = lambda: str(uuid.uuid1())

@server.route("/")
def default():
    return "<center><h1>Roman-Card-Game Server</h1></center>"

@server.route("/createRoom")
def createRoom():
    #try to find a match for public room
    if flask.request.form["public"] == "true":
        for id, room in allRooms.items():
            if room.public: #there exists an open public room
                room.public = False #close public room as it is taken
                room._eventCallback.set()
                return room.id
        else:
            id = generateID()
            event = threading.Event()
            allRooms[id] = Room(id, public=True, _eventCallback=event)

            event.wait()
            return id #return id of room

    else:
        if len(allRooms) >= 100:return "FULL" #no more space for another room

        #generate random string as room number, for example
        #741f8bd1-13a6-11ed-86a8-b05adaee0887
        id = generateID() 
        allRooms[id] = Room(id, public=False)
        return id

@server.route("/clean", methods=["GET", "POST"])
def clean():
    allRooms.clear()

@server.route("/openRooms")
def openRooms():
    return str(len(allRooms))

@socketIO.on("/joinRoom")
def joinRoom(data):
    #add connection to server's room list
    id = data["id"]
    userName = data["userName"]
    sid = flask.request.sid
    return allRooms[id].addClient(userName, sid)

if __name__ == "__main__":
    socketIO.run(server, host="0.0.0.0")
