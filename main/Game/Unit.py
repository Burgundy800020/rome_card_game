#units types
MAIN = 0
AUX = 1

class Unit:
    def __init__(self, ap, avail):
        self.ap = ap
        self.available = avail   #boolean
        

class Legionary(Unit):
    def __init__(self, ap=2, avail = False):
        super(Legionary, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3

class Cavalry(Unit):
    def __init__(self, ap=1, avail = False):
        super(Cavalry, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3

class Archery(Unit):
    def __init__(self, ap=1, avail = False):
        super(Archery, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3

class Velite(Unit):
    def __init__(self, ap=1, avail = False):
        super(Velite, self).__init__(self, ap, avail)
        self.type = AUX
        self.maxAp = 2

class Slinger(Unit):
    def __init__(self, ap=1, avail = False):
        super(Slinger, self).__init__(self, ap, avail)
        self.type = AUX
        self.maxAp = 2


if __name__ == "__main__":
    u = Unit()
    print(u.__dict__) 