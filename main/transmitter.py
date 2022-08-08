import threading
import socketio, requests

SERVER = "http://127.0.0.1:5000"
#SERVER = "http://roman-card-game.herokuapp.com/"
sio = socketio.Client()
sio.connect(SERVER)

class Room:
    def __init__(self):
        self.id = ""
    
    def join(self, id):
        self.id = id
        threading.Thread(target=sio.on(f"{id}/fromServer"), args=(self.listen, )).start()
    
    def listen(self, data):
        pass

    def send(self, data):
        sio.emit(f"{self.id}/fromServer", data=data)

class Transmitter:
    def __init__(self):
        self.room = Room()

    def createRoom(self):
        response = requests.get(f"{SERVER}/createRoom", data={}).text

        #No more space available for another room
        if response == "FULL":
            return

        return response #return room's id
    
    def joinRoom(self, userName, id):
        #send joining request to server
        sio.emit("joinRoom", data={"userName":userName, "id":id})
        self.room.join(id)
    
    def drawCard(self, n):
        pass

if __name__ == "__main__":
    t = Transmitter()
    id = t.createRoom()
    t.joinRoom("Crassus", id)
    print(id)