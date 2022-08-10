import uuid, threading
import flask, flask_socketio
import Game

#initialize flask server and socket units websocket
#server deployed to -> https://roman-card-game.herokuapp.com/
server = flask.Flask(__name__)
socketIO = flask_socketio.SocketIO(server)

class Room:
    def __init__(self, id, public=False):
        self.id = id
        self.public = public #room visibility for players looking for an opponent
        self.clients = []

        
        #listen for messages from client
        threading.Thread(target=socketIO.on(f"{id}/drawCard"), args=(self.drawCard, )).start()

        #initialize game instance
        self.game = Game.GameManager()
    
    def addClient(self, userName, sid):
        #cannot add more than 2 players
        if len(self.clients) < 2:
            self.clients.append(sid)

            #send 2 character choices to player
            self.send("getCharacterChoices", {"characters":self.game.generateCharacters()}, sid)
        else:
            return
    
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
    if len(allRooms) >= 100:return "FULL" #no more space for another room

    #generate random string as room number, for example
    #741f8bd1-13a6-11ed-86a8-b05adaee0887
    id = generateID()
    allRooms[id] = Room(id, public=flask.request.data.form["public"])
    return id

@server.route("/clean")
def clean():
    allRooms.clear()

@socketIO.on("joinRoom")
def joinRoom(data):
    #add connection to server's room list
    id = data["id"]
    userName = data["userName"]
    sid = flask.request.sid
    allRooms[id].addClient(userName, sid)

if __name__ == "__main__":
    socketIO.run(server, host="0.0.0.0")
