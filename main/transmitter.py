import time, threading
import socketio, requests

def show(*args, **kwargs):
    print(args, kwargs)

#SERVER = "https://roman-card-game.herokuapp.com/"
#SERVER = "http://172.29.3.131:5000"
SERVER = "http://192.168.1.8:5000"

class Client(socketio.Client):
    def __init__(self):
        super(Client, self).__init__(self)
        self.connect(SERVER)

        self.id = requests.get(f"{SERVER}/createRoom", data={"public":"true"}).text
        print(self.id)

        self.emit(f"joinRoom", data={"id":self.id}, callback=lambda *args, **kwargs:show(args, kwargs))
        threading.Timer(5, self.kill).start()
    
    def kill(self):
        print("disconnecting")
        self.disconnect()

clients = []
for i in range(2):
    clients.append(Client())