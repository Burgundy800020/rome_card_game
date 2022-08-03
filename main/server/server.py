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
                
                #break down messages into keywords
                message = message.split(" ")

                if message[0] == "ADD":
                    port = self.open_room()
                    if port==None:
                        connexion.send(b"Low Bandwidth")
                    else:
                        connexion.send(f"{port}".encode())
                
                elif message[0] == "ID":
                    url, open_port = self.get_room_id(int(message[1]))
                    connexion.send(f"{url}:{open_port}".encode())
            except:
                continue
    
    def get_room_id(self, port):
        room = self.all_rooms[port]
        return room.url, room.open_port
    
    def open_room(self):
        for i in range(1, 65536):
            if i not in self.all_rooms:
                port = i
                break
        else:# no more bandwidth available for another room
            return
        self.all_rooms[port] = Room(port)
        return port
    
    def close_room(self, port):
        room = self.all_rooms[port]
        room.close_room()
        ngrok.disconnect(get_url(room.url, room.open_port))
        del self.all_rooms[port]

class Room(socket.socket):
    def __init__(self, port):
        self.url, self.open_port = parse_url(ngrok.connect(port, "tcp").public_url)
        super(Room, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.bind(("", port))
        self.listen()

        start_new_thread(self.accept_connexion, ())

        self.clients = []

    def accept_connexion(self):
        while True:
            connexion, address = self.accept()
            self.clients.append(connexion)
            start_new_thread(self.listen_client, (connexion, address))
        
    def listen_client(self, connexion, address):
        while True:
            message = connexion.recv(32).decode()
    
    def remove_client(self, connexion):
        connexion.close()
        self.clients.remove(connexion)
    
    def close_room(self):
        while self.clients:
            self.remove_client(self.clients[0])
        self.close()

server = Server()

#Prevent main thread from exiting
if __name__ == "__main__":
    while True:input()