from typing import List
import uuid, threading
import flask, flask_socketio
import Game

#test comment a

#initialize flask server and socket units websocket
#server deployed to -> https://roman-card-game.herokuapp.com/
server = flask.Flask(__name__)
socketIO = flask_socketio.SocketIO(server)

class Room:
    def __init__(self, id, public=False, _eventCallback=None):
        self.id = id
        self.public = public #room visibility for players looking for an opponent
        self._eventCallback = _eventCallback #internal variable
        self.clients = {} #dictionnary: sid maps to character object

        #initialize game instance
        self.game = Game.GameManager(self, socketIO)

        """socketIO.on(f"{id}/drawCard")(self.drawCard)
        socketIO.on(f"{id}/discardCard")(self.discardCard)"""
        socketIO.on(f"{id}/setCharacterChoice")(self.setCharacterChoice)
    
    def addClient(self, sid):
        #cannot add more than 2 players
        if len(self.clients) < 2:
            self.clients[sid] = None
        else:
            return "FULL"

        if len(self.clients) == 2:

            if not self.public:
                #notify first client that a second one connected
                #only in private mode
                self.send("establishPrivateConnection", {}, list(self.clients.keys())[0])

            for sid in self.clients.keys():
                #send 2 character choices to each player
                self.send("getCharacterChoices", {"characters":self.game.generateCharacters()}, sid)

        return "ACCEPTED" #return empty string if completed successfully
    
    def removeClient(self, sid):
        #remove client
        #return true if client in list else false
        try:
            del self.clients[sid]
        except KeyError:
            return False
        return True
            
    def send(self, route, data, sid):
        socketIO.emit(route, data=data, room=sid)
    
    ######## listening commands from client ########
    def setCharacterChoice(self, data):
        sid = flask.request.sid
        character = self.game.addPlayer(data["character"], sid=sid)
        self.clients[sid] = character

        #check if both characters are set
        if not None in self.clients.values():

            #set opponent parameter in Player object
            playerlist = list(self.clients.values())
            playerlist[0].opp = playerlist[1]
            playerlist[1].opp = playerlist[0]

            #notify both players when game is starting
            for sid in self.clients.keys():
                self.send("startGame", {}, sid=sid)

            self.game.play()
    
    #using the drawCard method in gameManager
    """
    def drawCard(self, data):
        #draw a given number of card for a given character and return hand
        sid = flask.request.sid
        character = self.clients[sid]
        character.draw(data["n"])

        #inform opponent about the number of card left in hand
        hand = character.handToJson()
        self.send("opponentCard", {"n":len(hand)}, character.opp.sid)
        return hand

    def discardCard(self, data):
        #given an array of cards indexes, delete the cards correponding to the indexes
        sid = flask.request.sid
        character = self.clients[sid]
        character.discard(data["n"])
        
        hand = character.handToJson()
        self.send("opponentCard", {"n":len(hand)}, character.opp.sid)
        return hand
    """

    def close(self):
        socketIO.close_room(f"{id}/drawCard")

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

            #wait till another user joins the empty room to return new room's id
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
    for room in allRooms.values():
        room.close()
    allRooms.clear()
    return ""

@server.route("/deleteRoom")
def deleteRoom():
    id = flask.request.data["id"]
    allRooms[id].close()
    del allRooms[id]
    return ""

@server.route("/openRooms")
def openRooms():
    return str(len(allRooms))

@server.route("/userInRoom")
def userInRoom():
    #return number of clients already connected to an open room
    #prevents more than 2 users to connect
    id = flask.request.form["id"]
    return str(len(allRooms[id].clients))

@socketIO.on("joinRoom")
def joinRoom(data):
    #add connection to server's room list
    id = data["id"]
    sid = flask.request.sid
    return allRooms[id].addClient(sid)

@socketIO.on("disconnect")
def disconnect():
    #get called automatically when someone disconnects from the server
    sid = flask.request.sid
    for room in allRooms.values():
        if room.removeClient(sid): #client got removed

            if len(room.clients) == 0: #all clients left the room; delete room
                room.close()

            break

if __name__ == "__main__":
    socketIO.run(server, host="0.0.0.0")
