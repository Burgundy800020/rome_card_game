import socket
from _thread import *

class Transmitter(socket.socket):
    host = "192.168.1.237"

    def __init__(self):
        #connect to server
        super(Transmitter, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, 801))

    def new_room(self):
        self.send(b"ADD")
        ip, port = self.parse_room(self.recv(36))
    
    def parse_room(self, info:bytes):
        #b"192.168.1.237:1233"
        info = info.decode()
        ip, port = info.split(":")
        return ip, int(port)

if __name__ == "__main__":
    t = Transmitter()