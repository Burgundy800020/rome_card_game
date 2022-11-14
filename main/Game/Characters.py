from random import choices
from . import Card as c, Unit as u
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
        
        #debuffs
        self.sieged = False
        self.panemed = False

        #counters
        self.itemLimit = self.PoliticalLimit = 1
        self.handLimit = 4
        self.resetCount()
    
    def resetCount(self):
        #reset counters for item cards and strategy cards played during a turn
        self.itemPlayed = self.PoliticalPlayed = 0
    def unitsToJson(self):
        return [unit.toJson() for unit in self.units]

    def handToJson(self):
        return [card.toJson() for card in self.hand]
    #basic actions
    """
    def draw(self,n):
        #chose cards from deck and initialize
        for i in range(n):
            card = choices(self.deck, weights=self.weights, k=1).pop()()
            self.hand.append(card)

    def discard(self, n:list):
        n.sort(reverse=True)
        for i in n:
            del self.hand[i]     """ 


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
        self.handLimit = 5
        


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