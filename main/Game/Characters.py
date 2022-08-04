CONSUL = 0
GENERAL = 1
REBEL = 2
ENEMY = 3

allRoles = [CONSUL, GENERAL, REBEL, ENEMY]

class Player:
    def __init__(self, game, role):
        self.game = game
        self.hp = 6
        self.hand = []
        self.units = []
        self.name = ""
        self.role = role
        
        self.playing = False

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
        self.hand.addAll(self.game.generateCard(2))


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

romans = [Crassus, Caesar, Cicero, Pompeius]
enemies = [Hannibal]