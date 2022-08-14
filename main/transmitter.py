import socketio, requests

def show(args, kwargs):
    print(args, kwargs)

#SERVER = "https://roman-card-game.herokuapp.com/"
SERVER = "http://192.168.1.6:5000"
sio = socketio.Client()
sio.connect(SERVER)

id = requests.get(f"{SERVER}/createRoom", data={"public":"false"}).text
print(id)

requests.get(f"{SERVER}/clean")
sio.emit(f"{id}/drawCard", data={"n":10})
sio.emit(f"joinRoom", data={"id":id, "userName":"Crassus"}, callback=lambda *args, **kwargs:show(args, kwargs))

print("\n\n")
print(requests.get(f"{SERVER}/openRooms").text)
