from random import randint

#Card types
ITEM = 0
UNIT = 1
MILITARY = 2
POLITICAL = 3


class Card:
    def __init__(self):
        self.numeral = randint(1, 6)
        self.available = True

    def toJson(self):
        #convert card into json format
        return {
            "type":self.type,
            "numeral":self.numeral,
            "available":self.available}
    
    def fromJson(self, data):
        #load card information from json data
        self.type = data["type"]
        self.numeral = data["numeral"]
        self.available = data["available"]

class Shield(Card):
    def __init__(self):
        super(Shield, self).__init__()
        self.type = ITEM
        

class Horse(Card):
    def __init__(self):
        super(Horse, self).__init__()
        self.type = ITEM

class Arrows(Card):
    def __init__(self):
        super(Arrows, self).__init__()
        self.type = ITEM


class Ration(Card):
    def __init__(self):
        super(Ration, self).__init__()
        self.type = ITEM

class Aquilifer(Card):
    def __init__(self):
        super(Aquilifer, self).__init__()
        self.type = ITEM



class Legionary(Card):
    def __init__(self):
        super(Legionary, self).__init__()
        self.type = UNIT


class Cavalry(Card):
    def __init__(self):
        super(Cavalry, self).__init__()
        self.type = UNIT

class Archery(Card):
    def __init__(self):
        super(Archery, self).__init__()
        self.type = UNIT

class Velite(Card):
    def __init__(self):
        super(Velite, self).__init__()
        self.type = UNIT

class Slinger(Card):
    def __init__(self):
        super(Slinger, self).__init__()
        self.type = UNIT

class Barbarian_Invasion(Card):
    def __init__(self):
        super(Barbarian_Invasion, self).__init__()
        self.type = MILITARY
    

class Testudo(Card):
    def __init__(self):
        super(Testudo, self).__init__()
        self.type = MILITARY

class Camp(Card):
    def __init__(self):
        super(Camp, self).__init__()
        self.type = MILITARY

class Siege(Card):
    def __init__(self):
        super(Siege, self).__init__()
        self.type = MILITARY

class Onager(Card):
    def __init__(self):
        super(Onager, self).__init__()
        self.type = MILITARY

class Reinforcements(Card):
    def __init__(self):
        super(Reinforcements, self).__init__()
        self.type = MILITARY


class Senatus_Cousultum_Ultimum(Card):
    def __init__(self):
        super(Senatus_Cousultum_Ultimum, self).__init__()
        self.type = POLITICAL

class Veto(Card):
    def __init__(self):
        super(Veto, self).__init__()
        self.type = POLITICAL

class Land_Redistribution(Card):
    def __init__(self):
        super(Land_Redistribution, self).__init__()
        self.type = POLITICAL

class Election(Card):
    def __init__(self):
        super(Election, self).__init__()
        self.type = POLITICAL