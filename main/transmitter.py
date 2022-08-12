import socketio, requests

#SERVER = "https://roman-card-game.herokuapp.com/"
SERVER = "http://192.168.1.6:5000"

response = requests.get(f"{SERVER}/createRoom", data={"public":"true"}).text
print(response)

print("\n\n")
print(requests.get(f"{SERVER}/openRooms").text)