from random import shuffle, choices
import threading
from . import Card as c, Characters
#import Card, Characters

class GameManager:
    def __init__(self, server):
        self.server = server
        self.remRomans = Characters.characterList.copy(); shuffle(self.remRomans)
        self.deck = [c.Shield, c.Horse, c.Arrows]
        self.weights = [1,1,1]
        self.players = []
        self.currentPlayer = False
        self.playingTurn = threading.Event()
        self.discarding = threading.Event()
    
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
    
    #Basic actions

    def drawCard(self, character:Characters.Player, n):
        #modify player's hand in backend
        for i in range(n):
            card = choices(self.deck, weights=self.weights, k=1).pop()()
            self.hand.append(card)
        #update hand to both players
        hand = character.handToJson()
        self.server.send("playerCard", {"hand":hand}, character.sid)
        self.server.send("opponentCard", {"n":len(hand)}, character.opp.sid)

    def discardCard(self, character:Characters.Player, n):
        self.discarding.clear()
        self.server.send("playerDiscard", {"n": n}, character.sid)
        self.discarding.wait()
        #receive call back from frontend and modify player's hand in backend

        #update hand to both players
        hand = character.handToJson()
        self.server.send("playerCard", {"hand":hand}, character.sid)
        self.server.send("opponentCard", {"n":len(hand)}, character.opp.sid)



    def heal(self, character:Characters.Player, n):
        character.hp = min(character.hp + n, 10)
        self.server.send("playerHp", {"hp": character.hp}, character.sid)
        self.server.send("opponentHp", {"hp":character.hp}, character.opp.sid)
    
    #deal n damage to character
    #The damage is decisive if it results from a Legionary or Cavalry attack
    def dealDamage(self, character:Characters.Player, n, decisive=False):
        if character.hp > n:
            character.hp -= n
        elif not decisive:
            character.hp = 1
        else:
            #gameover
            pass

        #update hp to both players
        self.server.send("playerHp", {"hp": character.hp}, character.sid)
        self.server.send("opponentHp", {"hp":character.hp}, character.opp.sid)

    
    def play(self):
        while True:
            #self.playingTurn.clear()

            #fetch current player
            player = self.players[self.currentPlayer]
            #self.server.send("playTurn", {}, sid=player.sid) #let player begin the turn

            #self.playingTurn.wait()
            self.playturn(player)
            self.currentPlayer = not self.currentPlayer #invert player
            break

    def playturn(self, player):
        self.preturn(player)
        self.drawphase(player)
        self.playphase(player)
        self.discardphase(player)
        self.battlephase(player)
        self.postturn(player)


    def preturn(self, player):
        pass

    def drawphase(self, player):
        self.drawCard(player, 2)

    def playphase(self, player):
        while True:
            break

    def discardphase(self, player):
        pass

    def battlephase(self, player):
        pass

    def postturn(self, player):
        self.resetCount()


if __name__ == "__main__":
    g = GameManager()
    print([c.name for c in g.generateCharacters(Characters.ENEMY)])