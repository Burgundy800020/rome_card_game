import sys
from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

sequence = 1
acknowledgeNumber = 1

@socketio.on("message")
def handle_message(data):
    global sequence, acknowledgeNumber

    # Process data received from client
    print(f"Received data: {data}")
    acknowledgeNumber += sys.getsizeof(data)
    sequence = data["_sequence"]

    # Send response
    emit(f"{sequence}/ack", {"_acknowledge": True,
                     "_acknowledgeNumber": acknowledgeNumber})

if __name__ == "__main__":
    socketio.run(app)