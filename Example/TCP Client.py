import socket
from _thread import *

class RoomClient(socket.socket):
    #Room's IP/port
    host = "192.168.1.6"
    port = 1

    def __init__(self):
        self.run = True
        #servers IP/port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(("192.168.1.6", 8008))

        super(RoomClient, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, self.port))
        start_new_thread(self.catchMessage, ())

        while self.run:
            message = input()
            self.send(bytes(message, "latin-1"))
    
    def kill(self):
        self.run = False
        self.close()
        exit()
    
    def catchMessage(self):
        while self.run:
            message = self.recv(1024)
            if message:
                print(f"Incoming message: {message.decode()}")
            else:
                self.kill()
client = RoomClient()
