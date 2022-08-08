from random import choices, shuffle
from . import Card as c
#import Card as c

class Player:
    def __init__(self, game):
        self.game = game
        self.opp = None
        self.hp = 9
        self.hand = []
        self.units = []
        self.name = ""
        
        self.deck = [c.Shield, c.Horse, c.Arrows]
        self.weights = [1,1,1]

        #counters
        self.itemLimit = self.PoliticalLimit = 1
        self.resetCount()
    
    def resetCount(self):
        #reset counters for item cards and strategy cards played during a turn
        self.itemPlayed = self.PoliticalPlayed = 0
        

    def playTurn(self):
        self.preturn()
        self.drawphase()
        self.playphase()
        self.discardphase()
        self.attackphase()
        self.postturn()


    def preturn(self):
        pass

    def drawphase(self):
        self.draw(2)

    def playphase(self):
        while True:
            pass

    def discardphase(self):
        pass

    def attackphase(self):
        pass

    def postturn(self):
        self.resetCount()
    
    #basic actions

    def draw(self,n):
        for i in range(n):
            card = choices(self.deck, weights=self.weights, k=1).pop()
            self.hand.append(card)
    

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

class Crassus(Player):

    name = "Marcus Licinius Crassus"

    def __init__(self, game):
        super(Crassus, self).__init__(game)
        
    def drawphase(self):
        self.draw(3)


class Caesar(Player):
    
    name = "Caius Julius Caesar" 


    def __init__(self, game):
        super(Caesar, self).__init__(game)



class Cicero(Player):

    name = "Marcus Tullius Cicero"

    def __init__(self, game):
        super(Cicero, self).__init__(game)


class Pompeius(Player):
    
    name = "Gnaeus Pompeius Magnus" 

    def __init__(self, game):
        super(Pompeius, self).__init__(game)


class Hannibal(Player):
    
    name = "Hannibal Barca" 

    def __init__(self, game):
        super(Pompeius, self).__init__(game)

romans = [Crassus, Caesar, Cicero, Pompeius, Hannibal]