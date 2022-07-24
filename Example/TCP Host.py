import socket
from _thread import *
from pyngrok import ngrok

commands = """
Available commands are:
1. ADD [room id] - add an additional room with specified id
2. REM [room id] - remove room with specified id
3. LST - list all existing rooms
4. QUIT - close all chat rooms and exit server
"""

class Room(socket.socket):
    addr = ""

    def __init__(self, port, url="", openPort=8008):
        self.port = port
        self.url = url
        self.openPort = openPort
        
        super(Room, self).__init__(socket.AF_INET, socket. SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((self.addr, self.port))
        self.listen(100)

        self.clients = []
        start_new_thread(self.acceptConnection, ())

    def acceptConnection(self):
        while True:
            try:
                connection, addr = self.accept()
                self.clients.append(connection)
                start_new_thread(self.clientThread, (connection, addr))
            except:
                break
    
    def remove(self, client):
        client.close()
        self.clients.remove(client)
    
    def kill(self):
        while self.clients:
            self.remove(self.clients[0])
        self.close()

    def broadcast(self, message, connection):
        for client in self.clients:
            if client != connection:
                try:
                    client.send(bytes(message))
                except:
                    pass
    
    def clientThread(self, connection, addr):
        connection.send(bytes(f"Welcome to chatroom {self.port}!", "latin-1"))
        while True:
            try:
                message = connection.recv(1024)
                if message:
                    print(f"From {addr}: {message.decode()}")
                    self.broadcast(message, connection)
                else:
                    self.remove(connection)
            except:
                pass

class Server(socket.socket):
    def __init__(self):
        super(Server, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(("", 8008))
        self.listen(100)
        start_new_thread(self.acceptConnection, ())

        self.rooms = {}
        self.url, self.openPort = self.parseUrl(ngrok.connect(8008, "tcp").public_url)
        print(f"Server running on {self.url} port {self.openPort}")
    
    def acceptConnection(self):
        while True:
            try:
                connection, addr = self.accept()
                start_new_thread(self.clientThread, (connection, addr))
                print(f"Client {addr} connected.")
            except:
                break
    
    def clientThread(self, connection, addr):
        while True:
            try:
                message = connection.recv(1024)
                if message:
                    pass
                else:
                    connection.close()
            except:
                continue
        
    def parseUrl(self, url:str):
        url, port = url.split("//").pop().split(":")
        return url, int(port)
    
    def getUrl(self, url:str, port:int):
        return f"tcp://{url}:{port}"

    def addRoom(self, port):
        if port in self.rooms:
            print(f"Room {port} is already open.")
            return
        url, openPort = self.parseUrl(ngrok.connect(port, "tcp").public_url)
        self.rooms[port] = Room(port, url=url, openPort=openPort)
        print(f"New room {port} is now available at {url} on port {openPort}")

    def removeRoom(self, port):
        room = self.rooms[port]
        ngrok.disconnect(self.getUrl(room.url, room.openPort))
        room.kill()
        del self.rooms[port]

print(commands)
server = Server()
server.addRoom(1)

while True:
    cmd = input()
    if cmd:
        cmd = cmd.split(" ")

        if cmd[0] == "ADD":
            try:server.addRoom(int(cmd[1]))
            except ValueError:print(f"Invalid room number: {cmd[1]}")
        elif cmd[0] == "REM":
            try:server.removeRoom(int(cmd[1]))
            except ValueError:print(f"Invalid room number: {cmd[1]}")
        elif cmd[0] == "LST":
            for i, s in enumerate(server.rooms):print(f"Room {i+1} - {s} - {len(server.rooms[s].clients)} users currently online")
        elif cmd[0] == "QUIT":
            for port in list(server.rooms.keys()):
                server.removeRoom(port)
            print("All rooms correctly terminated.")
            exit()

        else:
            print(f"Unrecognized command: {cmd[0]}")
