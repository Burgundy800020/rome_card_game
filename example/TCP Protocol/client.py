import threading, time
import socketio

server = "http://127.0.0.1:5000"
sio = socketio.Client()
TIMEOUT = 3

sequence = 1

#establish connection to server
sio.connect(server)

class TimeoutEvent(threading.Event):
    def __init__(self):
        super().__init__()
        self._timeout = None
        self._start_time = None

    def wait_timeout(self, timeout):
        self._timeout = timeout
        self._start_time = time.monotonic()
        with self._cond:
            while not self.is_set():
                if self._timed_out():
                    return False
                self._cond.wait(self._remaining_time())
        return True

    def _timed_out(self):
        return self._remaining_time() <= 0

    def _remaining_time(self):
        if self._timeout is None:
            return float("inf")
        return self._timeout - (time.monotonic() - self._start_time)

    def set(self):
        super().set()
        if self._timeout is not None:
            with self._cond:
                self._cond.notify_all()
            self._timeout = None

def send_data(data:dict):
    #append header to message
    data["_sequence"] = sequence
    
    print(f"Sending data: {data}")
    sio.emit("message", data)

    #wait for confirmation
    event = TimeoutEvent()
    sio.on(f"{sequence}/ack", lambda data: listenAcknowledge(event, data))
    if event.wait_timeout(TIMEOUT):return
    else:send_data("message", data)

def listenAcknowledge(event, data):
    global sequence
    print(data)
    event.set()
    sequence = data["_acknowledgeNumber"]

send_data({"text": "Hello World!"})
