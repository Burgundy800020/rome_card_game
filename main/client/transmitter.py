import socket
from _thread import *

class Transmitter(socket.socket):
    host = "192.168.1.6"

    def __init__(self):
        #connect to server
        super(Transmitter, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, 801))

    def new_room(self):
        self.send(b"ADD")
        response = self.recv(32).decode()

        if response == "Low Bandwidth":
            return

        ip, port = self.parse_room(response)
        print(f"Connected to {ip} via port {port}")
    
    def parse_room(self, info:str):
        #b"192.168.1.237:1233"s
        info = info
        ip, port = info.split(":")
        return ip, int(port)

if __name__ == "__main__":
    t = Transmitter()
    t.new_room()