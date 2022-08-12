import socketio, requests

#SERVER = "https://roman-card-game.herokuapp.com/"
SERVER = "http://192.168.1.6:5000"
sio = socketio.Client()
sio.connect(SERVER)

id = requests.get(f"{SERVER}/createRoom", data={"public":"false"}).text
print(id)

sio.emit(f"joinRoom", data={"id":id, "userName":"Crassus"})

print("\n\n")
print(requests.get(f"{SERVER}/userInRoom", data={"id":id}).text)
print(requests.get(f"{SERVER}/openRooms").text)