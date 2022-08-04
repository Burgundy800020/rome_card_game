import os,socketio,requests,threading

clearScreen=lambda:os.system("cls")
server="http://socketio-test-enris.herokuapp.com"
sio=socketio.Client()

class Room:
    def __init__(self,key,username):
        self.key=key
        self.username=username
        clearScreen()
        print(f"Welcome to room {self.key}\n")
        threading.Thread(target=sio.on(self.key+"/fromServer"),args=(self.listen,)).start()
        self.send()

    def listen(self,data):
        if data["username"]==self.username:pass
        elif data["username"]!="":print(f"{data['username']}: {data['message']}")
        else:print(data["message"])

    def send(self):
        while True:
            message=input()
            sio.emit(self.key+"/fromClient",data={"username":self.username,"message":message})

class Main:
    def __init__(self):
        while True:
            self.username=input("Enter your username: ")
            print("Contacting server...")
            if self.connect():self.menu()

    def connect(self):
        sio.connect(server)
        response=requests.get(server+"/connection",data={"username":self.username}).text
        if response=="approved":return True
        elif response=="username unavailable":print("This username is already in use.")
        else:print("We can't connect you at the time.")
        return False

    def createRoom(self):
        response=requests.get(server+"/createRoom").text
        if response=="full":print("The server is now full. Try again later.")
        self.joinRoom(response)

    def joinRoom(self,key):
        response=requests.get(server+"/joinRoom",data={"key":key,"username":self.username}).text
        if response=="approved":Room(key,self.username)
        else:print("The room key is invalid.")

    def askJoinRoom(self):
        key=input("Room Key: ")
        self.joinRoom(key)

    def menu(self):
        clearScreen()
        print(f"Welcome, {self.username}\nChoose an option from the list:\n  1.Create Room\n  2.Join Room")
        while True:
            try:
                command=int(input(">>"))
                assert command in [1,2]
            except:print("invalid command")
            if command==1:self.createRoom()
            elif command==2:self.askJoinRoom()
        
Main()
