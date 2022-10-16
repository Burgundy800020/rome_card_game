from random import choices
from . import Card as c
#import Card as c

class Player:
    def __init__(self, game, sid=""):

        self.game = game
        self.sid = sid

        self.opp = None
        self.hp = 10
        self.hand = []
        self.units = []
        self.name = ""
        

        #counters
        self.itemLimit = self.PoliticalLimit = 1
        self.handLimit = 4
        self.resetCount()
    
    def resetCount(self):
        #reset counters for item cards and strategy cards played during a turn
        self.itemPlayed = self.PoliticalPlayed = 0
        
    def handToJson(self):
        return [card.toJson() for card in self.hand]

    #basic actions
    """"
    def draw(self,n):
        #chose cards from deck and initialize
        for i in range(n):
            card = choices(self.deck, weights=self.weights, k=1).pop()()
            self.hand.append(card)

    def discard(self, n:list):
        n.sort(reverse=True)
        for i in n:
            del self.hand[i]     """

    def checkAvailableCards(self):
        #check available cards during play phase
        for card in self.hand:
            
            if card.type == c.ITEM:

                if self.itemPlayed >= self.itemLimit:
                    card.available = False

                elif isinstance(card, c.Shield):
                    card.available = True if any([isinstance(unit, c.Legionary) for unit in self.units]) else False
                
                elif isinstance(card, c.Horse):
                    card.available = True if any([isinstance(unit, c.Cavalry) for unit in self.units]) else False

                elif isinstance(card, c.Arrows):
                    card.available = True if any([isinstance(unit, c.Archery) for unit in self.units]) else False
                
                elif isinstance(card, c.Ration):
                    card.available = True

                elif isinstance(card, c.Aquilifer):
                    card.available = True if len(self.units) else False

            elif card.type == c.UNIT:
                card.avaiable = False if len(self.units) >= 3 else True

        
            elif card.type == c.MILITARY:

                if isinstance(card, c.Testudo):
                    card.available = False

                elif isinstance(card, c.Camp):
                    card.available = True if len(self.units) else False

                else:
                    card.available = True

            else: #remaining card type: political
                if self.politicalPlayed >= self.politicalLimit:
                    card.available = False

                elif isinstance(card, c.Recrutement):
                    card.available = False if len(self.units) >= 3 else True

                elif isinstance(card, c.Rebellion):
                    card.available = True if len(self.opp.units) and len(self.units) < 3 else False

                elif isinstance(card, c.Veto):
                    card.available = False

                else:
                    card.available = True

    def toJson(self):
        return {"name":self.name}

class Marius(Player):

    name = "Caius Marius"

    def __init__(self, game, **kwargs):
        super(Marius, self).__init__(game, **kwargs)
        
class Sulla(Player):

    name = "Lucius Cornelius Sulla"

    def __init__(self, game, **kwargs):
        super(Sulla, self).__init__(game, **kwargs)
        

class Crassus(Player):

    name = "Marcus Licinius Crassus"

    def __init__(self, game, **kwargs):
        super(Crassus, self).__init__(game, **kwargs)
        


class Caesar(Player):
    
    name = "Caius Julius Caesar" 


    def __init__(self, game, **kwargs):
        super(Caesar, self).__init__(game, **kwargs)



class Pompeius(Player):
    
    name = "Gnaeus Pompeius Magnus" 

    def __init__(self, game, **kwargs):
        super(Pompeius, self).__init__(game, **kwargs)


class Vercingetorix(Player):
    
    name = "Vercingetorix" 

    def __init__(self, game, **kwargs):
        super(Vercingetorix, self).__init__(game, **kwargs)

class Mithridates(Player):
    
    name = "Mithridates" 

    def __init__(self, game, **kwargs):
        super(Mithridates, self).__init__(game, **kwargs)

class Surena(Player):
    
    name = "Surena" 

    def __init__(self, game, **kwargs):
        super(Surena, self).__init__(game, **kwargs)

characterList = [Caesar, Vercingetorix, Pompeius, Crassus]
nameList = [p.name for p in characterList]