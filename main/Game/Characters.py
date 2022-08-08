from random import choices, shuffle
import Card as c

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
        self.resetCount()
    
    def resetCount(self):
        #reset counters for item cards and strategy cards played during a turn
        self.itemPlayed = self.strategyPlayed = 0

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
            
            if card.type == 
            

                if isinstance(card, c.Shield):
                    card.available = True if any([isinstance(unit, c.Legionary) for unit in self.units]) else False
                
                elif isinstance(card, c.Horse):
                    card.available = True if any([isinstance(unit, c.Cavalry) for unit in self.units]) else False

                elif isinstance(card, c.Arrows):
                    card.available = True if any([isinstance(unit, c.Archery) for unit in self.units]) else False

            

            

class Crassus(Player):

    name = "Marcus Licinius Crassus"

    def __init__(self, game, role):
        super(Crassus, self).__init__(game, role)
        


class Caesar(Player):
    
    name = "Caius Julius Caesar" 


    def __init__(self, game, role):
        super(Caesar, self).__init__(game, role)



class Cicero(Player):

    name = "Marcus Tullius Cicero"

    def __init__(self, game, role):
        super(Cicero, self).__init__(game, role)


class Pompeius(Player):
    
    name = "Gnaeus Pompeius Magnus" 

    def __init__(self, game, role):
        super(Pompeius, self).__init__(game, role)


class Hannibal(Player):
    
    name = "Hannibal Barca" 

    def __init__(self, game, role):
        super(Pompeius, self).__init__(game, role)

romans = [Crassus, Caesar, Cicero, Pompeius, Hannibal]