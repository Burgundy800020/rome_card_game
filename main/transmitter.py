import time
import socketio, requests

def show(*args, **kwargs):
    print(args, kwargs)

#SERVER = "https://roman-card-game.herokuapp.com/"
SERVER = "http://192.168.1.6:5000"
sio = socketio.Client()
sio.connect(SERVER)

id = requests.get(f"{SERVER}/createRoom", data={"public":"false"}).text
print(id)

sio.emit(f"joinRoom", data={"id":id}, callback=lambda *args, **kwargs:show(args, kwargs))
sio.emit(f"joinRoom", data={"id":id}, callback=lambda *args, **kwargs:show(args, kwargs))
time.sleep(.5)

sio.emit(f"{id}/setCharacterChoice", data={"character":"Caius Julius Caesar"})
sio.emit(f"{id}/setCharacterChoice", data={"character":"Marcus Licinius Crassus"})
time.sleep(.5)

sio.emit(f"{id}/drawCard", data={"n":5}, callback=show)

print("Rooms open: " + requests.get(f"{SERVER}/openRooms").text)
