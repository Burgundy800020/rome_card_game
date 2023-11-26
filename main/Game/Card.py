from random import randint

#Card types
ITEM = 0
UNIT = 1
MILITARY = 2
POLITICAL = 3


class Card:
    frq = 0
    def __init__(self, name = ""):
        self.numeral = randint(1, 6)
        self.name = name
        self.type = None
        self.available = False

    def toJson(self):
        #convert card into json format
        return {
            "name":self.name,
            "numeral":self.numeral,
            "type":self.type
            }
    
    def fromJson(self, data):
        #load card information from json data
        self.name = data["name"]
        self.numeral = data["numeral"]
        self.type = data["type"]

class Shield(Card):
    frq = 10
    def __init__(self):
        super(Shield, self).__init__()
        self.name = "shield"
        self.type = ITEM
        

class Horse(Card):
    frq = 4
    def __init__(self):
        super(Horse, self).__init__()
        self.name = "horse"
        self.type = ITEM


class Arrows(Card):
    frq = 4
    def __init__(self):
        super(Arrows, self).__init__()
        self.name = "arrows"
        self.type = ITEM


class Ration(Card):
    frq = 4
    def __init__(self):
        super(Ration, self).__init__()
        self.name = "ration"
        self.type = ITEM

class Aquilifer(Card):
    frq = 3
    def __init__(self):
        super(Aquilifer, self).__init__()
        self.name = "aquilifer"
        self.type = ITEM

class Legionary(Card):
    frq = 8
    def __init__(self):
        super(Legionary, self).__init__()
        self.name = "legionary"
        self.type = UNIT


class Cavalry(Card):
    frq = 4
    def __init__(self):
        super(Cavalry, self).__init__()
        self.name = "cavalry"
        self.type = UNIT

class Archery(Card):
    frq = 4
    def __init__(self):
        super(Archery, self).__init__()
        self.name = "archery"
        self.type = UNIT

class Velite(Card):
    frq = 2
    def __init__(self):
        super(Velite, self).__init__()
        self.name = "velite"
        self.type = UNIT

class Slinger(Card):
    frq = 2
    def __init__(self):
        super(Slinger, self).__init__()
        self.name = "slinger"
        self.type = UNIT

class Barbarian_Invasion(Card):
    frq = 4
    def __init__(self):
        super(Barbarian_Invasion, self).__init__()
        self.name = "barbarian_invasion"
        self.type = MILITARY
    

class Testudo(Card):
    frq = 6
    def __init__(self):
        super(Testudo, self).__init__()
        self.name = "testudo"
        self.type = MILITARY

class Camp(Card):
    frq = 4
    def __init__(self):
        super(Camp, self).__init__()
        self.name = "camp"
        self.type = MILITARY

class Siege(Card):
    frq = 4
    def __init__(self):
        super(Siege, self).__init__()
        self.name = "siege"
        self.type = MILITARY

class Onager(Card):
    frq = 4
    def __init__(self):
        super(Onager, self).__init__()
        self.name = "onager"
        self.type = MILITARY

class Reinforcements(Card):
    frq = 3
    def __init__(self):
        super(Reinforcements, self).__init__()
        self.name = "reinforcements"
        self.type = MILITARY


class Senatus_Cousultum_Ultimum(Card):
    frq = 1
    def __init__(self):
        super(Senatus_Cousultum_Ultimum, self).__init__()
        self.name = "senatus_consultum_ultimum"
        self.type = POLITICAL

class Veto(Card):
    frq = 5
    def __init__(self):
        super(Veto, self).__init__()
        self.name = "veto"
        self.type = POLITICAL

class Land_Redistribution(Card):
    frq = 4
    def __init__(self):
        super(Land_Redistribution, self).__init__()
        self.name = "land_redistribution"
        self.type = POLITICAL

class Election(Card):
    frq = 0
    def __init__(self):
        super(Election, self).__init__()
        self.name = "election"
        self.type = POLITICAL

class Panem_Et_Circenses(Card):
    frq = 4
    def __init__(self):
        super(Panem_Et_Circenses, self).__init__()
        self.name = "panem_et_circenses"
        self.type = POLITICAL

class Urban_Construction(Card):
    frq = 3
    def __init__(self):
        super(Urban_Construction, self).__init__()
        self.name = "urban_construction"
        self.type = POLITICAL

