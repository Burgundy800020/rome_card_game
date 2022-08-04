import threading
import socketio, requests

SERVER = "https://127.0.0.1:5000"
sio = socketio.Client()
sio.connect(SERVER)

class Room:
    def __init__(self):
        self.id = ""
        self.listenProcess = None
    
    def join(self, id):
        self.id = id
        self.listenProcess = threading.Thread(target=sio.on(f"{id}/fromServer"), args=(self.listen, ))
        self.listenProcess.start()
    
    def listen(self, data):
        pass

class Transmitter:
    def __init__(self):
        self.room = Room()

    def createRoom(self):
        response = requests.get(f"{SERVER}/createRoom", data={}).text

        #No more space available for another room
        if response == "FULL":
            return

        return response #return room's id
    
    def joinRoom(self, id):
        #send joining request to server
        sio.emit("joinRoom", data={"id":id})
        self.room.join(id)

if __name__ == "__main__":
    t = Transmitter()
    id = t.createRoom()
    t.joinRoom(id)
    print(id)