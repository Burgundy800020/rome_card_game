from random import choices, shuffle
from . import Card, Characters
#import Card, Characters

class GameManager:
    def __init__(self):
        self.players = []
        self.dpile = []
        self.rolesRemaining = Characters.allRoles.copy(); shuffle(self.rolesRemaining)
        self.remRomans = Characters.romans.copy(); shuffle(self.remRomans)
        self.remEnemies = Characters.enemies.copy(); shuffle(self.remEnemies)
    
    def reset(self):
        pass;            

    def addPlayer(self, role, character):
        self.players.append(character(self, role))

    def generateRole(self):
        return self.rolesRemaining.pop()
    
    def generateCharacters(self, role):
        if role == Characters.ENEMY:
            characterChoices = self.remEnemies[:2]
            self.remEnemies = self.remEnemies[2:] 

        else:
            characterChoices = self.remRomans[:2]
            self.remRomans = self.remRomans[2:]

        return characterChoices

    def generateCard(self, n):
        return [card() for card in choices(Card.cards, weights=Card.weights, k=n)]

if __name__ == "__main__":
    g = GameManager()
    print([c.name for c in g.generateCharacters(Characters.ENEMY)])