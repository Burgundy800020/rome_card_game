from random import randint

#Card types
ITEM = 0
UNIT = 1
MILITARY = 2
POLITICAL = 3


class Card:
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
    def __init__(self):
        super(Shield, self).__init__()
        self.name = "shield"
        self.type = ITEM
        

class Horse(Card):
    def __init__(self):
        self.name = "horse"
        super(Horse, self).__init__()
        self.type = ITEM



class Arrows(Card):
    def __init__(self):
        self.name = "arrows"
        super(Arrows, self).__init__()
        self.type = ITEM


class Ration(Card):
    def __init__(self):
        self.name = "ration"
        super(Ration, self).__init__()
        self.type = ITEM

class Aquilifer(Card):
    def __init__(self):
        self.name = "aquilifer"
        super(Aquilifer, self).__init__()
        self.type = ITEM



class Legionary(Card):
    def __init__(self):
        self.name = "legionary"
        super(Legionary, self).__init__()
        self.type = UNIT


class Cavalry(Card):
    def __init__(self):
        self.name = "cavalry"
        super(Cavalry, self).__init__()
        self.type = UNIT

class Archery(Card):
    def __init__(self):
        self.name = "archery"
        super(Archery, self).__init__()
        self.type = UNIT

class Velite(Card):
    def __init__(self):
        self.name = "velite"
        super(Velite, self).__init__()
        self.type = UNIT

class Slinger(Card):
    def __init__(self):
        self.name = "slinger"
        super(Slinger, self).__init__()
        self.type = UNIT

class Barbarian_Invasion(Card):
    def __init__(self):
        self.name = "barbarian_invasion"
        super(Barbarian_Invasion, self).__init__()
        self.type = MILITARY
    

class Testudo(Card):
    def __init__(self):
        self.name = "testudo"
        super(Testudo, self).__init__()
        self.type = MILITARY

class Camp(Card):
    def __init__(self):
        self.name = "camp"
        super(Camp, self).__init__()
        self.type = MILITARY

class Siege(Card):
    def __init__(self):
        self.name = "siege"
        super(Siege, self).__init__()
        self.type = MILITARY

class Onager(Card):
    def __init__(self):
        self.name = "onager"
        super(Onager, self).__init__()
        self.type = MILITARY

class Reinforcements(Card):
    def __init__(self):
        self.name = "reinforcements"
        super(Reinforcements, self).__init__()
        self.type = MILITARY


class Senatus_Cousultum_Ultimum(Card):
    def __init__(self):
        self.name = "senatus_consultum_ultimum"
        super(Senatus_Cousultum_Ultimum, self).__init__()
        self.type = POLITICAL

class Veto(Card):
    def __init__(self):
        self.name = "veto"
        super(Veto, self).__init__()
        self.type = POLITICAL

class Land_Redistribution(Card):
    def __init__(self):
        self.name = "land_redistribution"
        super(Land_Redistribution, self).__init__()
        self.type = POLITICAL

class Election(Card):
    def __init__(self):
        self.name = "election"
        super(Election, self).__init__()
        self.type = POLITICAL

class Panem_Et_Circenses(Card):
    def __init__(self):
        self.name = "panem_et_circenses"
        super(Panem_Et_Circenses, self).__init__()
        self.type = POLITICAL

class Urban_Construction(Card):
    def __init__(self):
        self.name = "urban_construction"
        super(Urban_Construction, self).__init__()
        self.type = POLITICAL