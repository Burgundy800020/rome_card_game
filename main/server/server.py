import socket
from _thread import *
from pyngrok import ngrok #grant global access to server

def parse_url(url):
    url, port = url.split("//").pop().split(":")
    return url, int(port)

def get_url(url, port):
    return f"tcp://{url}:{port}"

class Server(socket.socket):
    def __init__(self):
        self.url, self.open_port = parse_url(ngrok.connect(801, "tcp").public_url)
        print(f"Server running on url: {self.url} on port: {self.open_port}")
        super(Server, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(("", 801))
        self.listen()

        start_new_thread(self.accept_connexion, ())

        self.all_rooms = {}

    def accept_connexion(self):
        while True:
            connexion, address = self.accept()
            start_new_thread(self.listen_client, (connexion, address))

    def listen_client(self, connexion, address):
        while True:
            try:
                message = connexion.recv(1024).decode()

                if not message:
                    connexion.close()

                if message == "ADD":
                    url, port = self.open_room()
                    if url==None and port==None:
                        connexion.send(b"Low Bandwidth")
                    else:
                        connexion.send(f"{url}:{port}".encode())
            except:
                continue
    
    def open_room(self):
        for i in range(65536, 1):
            if i not in self.all_rooms:
                port = i
                break
        else:# no more bandwidth available for another room
            return None, None
        self.all_rooms[port] = Room(port)
        return self.url, self.open_port

class Room(socket.socket):
    def __init__(self, port):
        self.url, self.open_port = parse_url(ngrok.connect(port, "tcp").public_url)
        super(Server, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.bind(("", port))
        self.listen()

        start_new_thread(self.accept_connexion, ())

    def accept_connexion(self):
        while True:
            connexion, address = self.accept()
    


server = Server()