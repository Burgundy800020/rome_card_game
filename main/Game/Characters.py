class Player:
    CONSUL = 0
    GENERAL = 1
    REBEL = 2
    ENEMY = 3

    def __init__(self, game):
        self.game = game
        self.hp = 6
        self.hand = []
        self.units = []
        self.name = ""
        self.role = self.CONSUL

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
        pass

    def playphase(self):
        pass

    def discardphase(self):
        pass

    def attackphase(self):
        pass

    def postturn(self):
        pass


class Crassus(Player):

    name = "Marcus Licinius Crassus"

    def __init__(self):
        pass


class Caesar(Player):
    
    name = "Caius Julius Caesar" 

    def __init__(self):
        pass



class Cicero(Player):

    name = "Marcus Tullius Cicero"

    def __init__(self):
        pass


class Pompeius(Player):
    
    name = "Gnaeus Pompeius Magnus" 

    def __init__(self):
        pass
