#units types
MAIN = 0
AUX = 1

class Unit:
    def __init__(self, ap, avail):
        self.ap = ap
        self.available = avail   #boolean
    
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
        name = "legionary"
        super(Legionary, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3
        self.damage = 2

class Celtic(Legionary):
    def __init__(self, ap=2, avail = False):
        name = "celtic"
        super(Celtic, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3

class Phalanx(Legionary):
    def __init__(self, ap=2, avail = False):
        name = "phalanx"
        super(Phalanx, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3

class Gladiator(Legionary):
    def __init__(self, ap=2, avail = False):
        name = "gladiator"
        super(Gladiator, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3

class Cavalry(Unit):
    def __init__(self, ap=1, avail = False):
        name = "cavalry"
        super(Cavalry, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3
        self.damage = 3

class Elephant(Cavalry):
    def __init__(self, ap=1, avail = False):
        name = "elephant"
        super(Elephant, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3

class Archery(Unit):
    def __init__(self, ap=1, avail = False):
        name = "archery"
        super(Archery, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3
        self.damage = 1


class Mounted_Archer(Archery):
    def __init__(self, ap=1, avail = False):
        name = "mounted_archer"
        super(Mounted_Archer, self).__init__(self, ap, avail)
        self.type = MAIN
        self.maxAp = 3


class Velite(Unit):
    def __init__(self, ap=1, avail = False):
        name = "velite"
        super(Velite, self).__init__(self, ap, avail)
        self.type = AUX
        self.maxAp = 2

class Slinger(Unit):
    def __init__(self, ap=1, avail = False):
        name = "slinger"
        super(Slinger, self).__init__(self, ap, avail)
        self.type = AUX
        self.maxAp = 2


if __name__ == "__main__":
    u = Unit()
    print(u.__dict__) 