import uuid, Utils
import flask, flask_socketio
import Game

ROOMNUMBER = 100

#initialize flask server and socket units websocket
#server deployed to -> https://roman-card-game.herokuapp.com/
server = flask.Flask(__name__)
socketIO = flask_socketio.SocketIO(server)

class Room:
    def __init__(self, id, public=False, occupied=True, _eventCallback=None):
        self.id = id
        self.public = public #room visibility for players looking for an opponent
        self._eventCallback = _eventCallback #internal variable
        self.clients = {} #dictionnary: sid maps to character object
        self.occupied = occupied #new clients may be directed to this room

        #initialize game instance
        self.game = Game.GameManager(self, socketIO)

        socketIO.on(f"{id}/setCharacterChoice")(self.setCharacterChoice)


    
    def addClient(self, sid):
        #cannot add more than 2 players
        if len(self.clients) < 2:
            self.occupied = True
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
            for sid, player in self.clients.items():
                self.send("startGame", {}, sid=sid)
                self.send("setCharacterName", {"player":player.name, "opponent":player.opp.name, "playerFull":player.full, "opponentFull":player.opp.full}, sid)

            for player in playerlist:
                self.game.drawCard(player, 4)

            self.game.preturn(list(self.clients.values())[0])
    
    def close(self):
        #remove all clients in present room by clearing client dictionary
        self.clients.clear()
        self.game = Game.GameManager(self, socketIO)
        liberateRoom(self)

#-----------------SERVER-----------------
allRooms = {}
#new players waiting for a room
#queue contains tuple (threading event, public:bool)
queue = [] 
generateID = lambda: str(uuid.uuid1())

def liberateRoom(room):
    room.public = False
    room.occupied = False #make room visible

    if len(queue): #tell next player in queue that the room just got liberated
        event, _ = queue.pop(0)
        event.setInfo({"room":room})

@server.route("/")
def default():
    return """
        <center><h1>Roman-Card-Game Server</h1></center>
        <center>Running Status : Normal</center>
        """

@server.route("/stats")
def stats():
    def generateRoomInfo():
        html = """<table border=3px>
            <tr>
                <th><p>Room ID</p></th>
                <th><p>Is Public</p></th>
                <th><p>Is Occupied</p></th>
            </tr>
        """
        for id, rooms in allRooms.items():
            html += f"""
            <tr>
                <td><p>{id}</p></td>
                <td><p>{rooms.public}</p></td>
                <td><p>{rooms.occupied}</p></td>
            </tr>"""
        return html + r"\n</table>"

    return f"""
    <h1>Debugging Statistics</h1>
    <p>Clients in queue:{len(queue)}</p>
    <p>Room number limit: {ROOMNUMBER}</p>
    <p>Rooms open: {len(allRooms)}</p>
    {generateRoomInfo()}
    """

@server.route("/createRoom")
def createRoom():
    if flask.request.form["public"] == "true":
        for id, room in allRooms.items():
            if room.public: #there exists an open public room
                room.public = False #close public room as it is taken
                room.occupied = True
                room._eventCallback.set()
                return room.id
        
        else: #no public room open, search for unoccupied room
            for id, room in allRooms.items():
                if not room.occupied:
                    event = Utils.Event()
                    room._eventCallback = event #prepare room and make it detectable to other public players
                    room.occupied = True
                    room.public = True

                    #wait till another user joins the empty room to return new room's id
                    event.wait()
                    return id #return id of room
            
            else: #no public room, no unoccupied room
                if len(allRooms) >= ROOMNUMBER:
                    event = Utils.Event()
                    queue.append((event, True)) #add to queue. when a room is liberated, join the room

                    data = event.waitInfo() #an unoccupied room is now available
                    room = data["room"]
                    directJoin = data.get("directJoin", False)

                    if directJoin:
                        room.public = False
                        room._eventCallback.set()
                        return room.id

                    event = Utils.Event()
                    room = allRooms[id]
                    room._eventCallback = event #prepare room and make it detectable to other public players
                    room.public = True
                    room.occupied = True
                    
                    for player, public in queue:#look for second public player in queue
                        if public:
                            player.setInfo({"room":room, "directJoin":True})
                            break

                    event.wait()
                    return room.id

                else: #if room limit not exceeded, create new public room
                    id = generateID()
                    event = Utils.Event()
                    allRooms[id] = Room(id, public=True, _eventCallback=event)

                    #wait till another user joins the empty room to return new room's id
                    event.wait()
                    return id #return id of room

    else: #create private room
        for id, room in allRooms.items(): #search for unoccupied room
            if not room.occupied:
                room.occupied = True
                return room.id

        else:
            if len(allRooms) >= ROOMNUMBER:
                event = Utils.Event()
                queue.append((event, False)) #add to queue. when a room is liberated, join the room

                room = event.waitInfo()["room"] #take the freed room

                room.public = False
                return room.id

            else: #if room limit not exceeded, create new private room
                id = generateID()
                event = Utils.Event()
                allRooms[id] = Room(id, public=False)

                return id

@server.route("/clean", methods=["GET", "POST"])
def clean():
    for room in allRooms.values():
        room.close()
    return ""

@server.route("/closeRoom")
def closeRoom():
    id = flask.request.data["id"]
    allRooms[id].close()
    return ""

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
    #socketIO.run(server, host="0.0.0.0")
    socketIO.run(server)

