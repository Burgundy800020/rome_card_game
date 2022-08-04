from random import randint

class Card:
    #Card types
    ITEM = 0
    UNIT = 1
    MILITARY = 2
    POLITICAL = 3
    
    def __init__(self, name, numeral):
        self.name = name
        self.numeral = numeral


    def playCard(self):
        pass

class Shield(Card):
    def __init__(self):
        self.type = self.ITEM
        

class Horse(Card):
    def __init__(self):


class Arrows(Card):
    def __init    

        
cards = list(range(10))