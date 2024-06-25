import threading


class Event(threading.Event):
    """
    Create and release events similarly to threading.Event, but with the ability to transfer information as a dictionary.
    """
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        self.data = dict()
    
    def waitInfo(self):
        #return data on release
        self.wait()
        return self.data
    
    def setInfo(self, data:dict):
        #release while setting some data
        self.data = data
        self.set()