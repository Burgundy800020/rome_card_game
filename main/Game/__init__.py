from random import shuffle
from . import Card, Characters
#import Card, Characters

class GameManager:
    def __init__(self):
        self.remRomans = Characters.romans.copy(); shuffle(self.remRomans)
        self.players = []
    
    def reset(self):
        pass   

    def addPlayer(self, character):
        self.players.append(character(self))
    
    def generateCharacters(self):
        #take two first characters (and remove them) from list
        characterChoices = self.remRomans[:2]
        self.remRomans = self.remRomans[2:]
        return characterChoices

if __name__ == "__main__":
    g = GameManager()
    print([c.name for c in g.generateCharacters(Characters.ENEMY)])