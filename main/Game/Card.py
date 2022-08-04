from random import randint

class Card:
    #Card types
    ITEM = 0
    UNIT = 1
    MILITARY = 2
    POLITICAL = 3
    
    def __init__(self):
        self.numeral = randint(1, 6)


    def playCard(self):
        pass

class Shield(Card):
    def __init__(self):
        super(Shield, self).__init__()
        self.type = self.ITEM
        

class Horse(Card):
    def __init__(self):
        super(Horse, self).__init__()
        self.type = self.ITEM

class Arrows(Card):
    def __init__(self):
        super(Arrows, self).__init__()
        self.type = self.ITEM

        
cards = [Shield, Horse, Arrows]
weights = [1,1,1]
