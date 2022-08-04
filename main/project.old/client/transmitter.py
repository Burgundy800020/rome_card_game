import socket
from _thread import *

def parse_room(info:str):
    #ip address:open_port
    #"192.168.1.6:1233"
    info = info
    ip, open_port = info.split(":")
    return ip, int(open_port)

class Transmitter(socket.socket):
    host = "192.168.1.6"

    def __init__(self):
        #connect to server
        super(Transmitter, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, 801))

        #create instance of Room() to enter a room within the server
        self.room = Room()

    def new_room(self):
        self.send(b"ADD")
        response = self.recv(32).decode()

        if response == "Low Bandwidth":
            return #return None if all rooms are filled

        port = int(response)
        print(f"Newly opened room is {port}")
        return port #return room number
    
    def connect_room(self, port):
        #request room's url and port from server
        self.send(f"ID {port}".encode())
        url, open_port = parse_room(self.recv(32).decode())

        #establish connection
        self.room.connect_room(url, open_port)
        print(f"Connected to room {port}")

class Room(socket.socket):
    def __init__(self):
        super(Room, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect_room(self, url, open_port):
        self.connect((url, open_port))
        self.connected = True

if __name__ == "__main__":
    t = Transmitter()
    id = t.new_room()
    t.connect_room(id)