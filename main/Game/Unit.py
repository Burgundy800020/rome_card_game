#units types
MAIN = 0
AUX = 1

#play_event

class Unit:
    name = ""
    maxAp = 0
    def __init__(self, ap, avail):
        self.ap = ap
        self.available = avail   #boolean
        self.type = -1
    
    def toJson(self):
        #convert card into json format
        return {
            "name":self.name,
            "available":self.available,
            "ap" : self.ap}
    
    def fromJson(self, data):
        #load card information from json data
        self.type = data["type"]
        self.numeral = data["numeral"]
        self.available = data["available"]

class Legionary(Unit):
    def __init__(self, ap=2, avail = False):
        super(Legionary, self).__init__(ap, avail)
        self.name = "legionary"
        self.type = MAIN
        self.maxAp = 3
        self.damage = 2

class Celtic(Legionary):
    def __init__(self, ap=2, avail = False):
        super(Celtic, self).__init__(ap, avail)
        self.name = "celtic"
        self.type = MAIN
        self.maxAp = 3

class Phalanx(Legionary):
    def __init__(self, ap=2, avail = False):
        super(Phalanx, self).__init__(ap, avail)
        self.name = "phalanx"
        self.type = MAIN
        self.maxAp = 3

class Gladiator(Legionary):
    def __init__(self, ap=2, avail = False):
        super(Gladiator, self).__init__(ap, avail)
        self.name = "gladiator"
        self.type = MAIN
        self.maxAp = 3

class Cavalry(Unit):
    def __init__(self, ap=1, avail = False):
        super(Cavalry, self).__init__(ap, avail)
        self.name = "cavalry"
        self.type = MAIN
        self.maxAp = 3
        self.damage = 3

class Elephant(Cavalry):
    def __init__(self, ap=1, avail = False):
        super(Elephant, self).__init__(ap, avail)
        self.name = "elephant"
        self.type = MAIN
        self.maxAp = 3

class Archery(Unit):
    def __init__(self, ap=1, avail = False):
        super(Archery, self).__init__(ap, avail)
        self.name = "archery"
        self.type = MAIN
        self.maxAp = 3
        self.damage = 1


class Mounted_Archer(Archery):
    def __init__(self, ap=1, avail = False):
        super(Mounted_Archer, self).__init__(ap, avail)
        self.name = "mounted_archer"
        self.type = MAIN
        self.maxAp = 3


class Velite(Unit):
    def __init__(self, ap=1, avail = False):
        super(Velite, self).__init__(ap, avail)
        self.name = "velite"
        self.type = AUX
        self.maxAp = 2

class Slinger(Unit):
    def __init__(self, ap=1, avail = False):
        super(Slinger, self).__init__(ap, avail)
        self.name = "slinger"
        self.type = AUX
        self.maxAp = 2


if __name__ == "__main__":
    pass