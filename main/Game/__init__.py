from random import shuffle
from . import Card, Characters
#import Card, Characters

class GameManager:
    def __init__(self, server):
        self.server = server
        self.remRomans = Characters.characterList.copy(); shuffle(self.remRomans)
        self.players = []
    
    def reset(self):
        pass   

    def addPlayer(self, character, sid=""):
        player = Characters.characterList[Characters.nameList.index(character)](self, sid=sid)
        self.players.append(player)
        return player

    def generateCharacters(self):
        #take two first characters (and remove them) from list
        characterChoices = self.remRomans[:2]
        self.remRomans = self.remRomans[2:]
        return [character.name for character in characterChoices]
    
    def drawCard(self, character:Characters.Player, n):
        return character.draw(n)
    
    def play(self):
        pass

if __name__ == "__main__":
    g = GameManager()
    print([c.name for c in g.generateCharacters(Characters.ENEMY)])