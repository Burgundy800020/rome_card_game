from random import shuffle, choices
import threading
import flask, flask_socketio

from . import Card as c, Characters
#import Card, Characters



class GameManager:
    def __init__(self, room, socketIO):
        self.room = room
        self.socketIO = socketIO
        self.remRomans = Characters.characterList.copy(); shuffle(self.remRomans)
        self.deck = [c.Shield, c.Horse, c.Arrows]
        self.weights = [1,1,1]
        self.players = []
        self.currentPlayer = False

        #game
        self.playphaseOngoing = True

        #events
        self.playingTurn = threading.Event()
        self.discarding = threading.Event()
        self.playing = threading.Event()


        #listen to channels
        self.socketIO.on(f"{self.room.id}/discardCard")(self.discardCardListen)
        self.socketIO.on(f"{self.room.id}/playphase")(self.playphaseListen)

    
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
    
    #Basic card actions

    def drawCard(self, character:Characters.Player, n):
        #modify player's hand in backend
        for i in range(n):
            card = choices(self.deck, weights=self.weights, k=1).pop()()
            self.hand.append(card)
        #update hand to both players
        hand = character.handToJson()
        self.room.send("playerCard", {"hand":hand}, character.sid)
        self.room.send("opponentCard", {"n":len(hand)}, character.opp.sid)

    def discardCardListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        #remove cards from player's hand
        n = data["n"]
        n.sort(reverse=True)
        for i in n:
            del self.hand[i] 
        #update hand to both players
        hand = character.handToJson()
        self.room.send("playerCard", {"hand":hand}, character.sid)
        self.room.send("opponentCard", {"n":len(hand)}, character.opp.sid)
        self.discarding.set()
    
    def discardCardRequest(self, character:Characters.Player, n, next_event):
        self.room.send("discardInput", {"n": n}, character.sid)
        #receive call back from frontend and modify player's hand in backend
    
    #basic hp actions
    def heal(self, character:Characters.Player, n):
        character.hp = min(character.hp + n, 10)
        self.room.send("playerHp", {"hp": character.hp}, character.sid)
        self.room.send("opponentHp", {"hp":character.hp}, character.opp.sid)
    
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
        self.room.send("playerHp", {"hp": character.hp}, character.sid)
        self.room.send("opponentHp", {"hp":character.hp}, character.opp.sid)

    #card effects
    def playCard(self, player: Characters.Player, card: c.Card):
        if card.type == c.ITEM:
            pass
        elif card.type == c.UNIT:
            pass
        elif card.type == c.MILITARY:
            if isinstance(card, c.Barbarian_Invasion):
                n = []
                for unit in player.opp.units:
                    if unit.ap == 1:
                        n.append(unit)
                self.room.send("opponentUnitInput", {"n": n}, player.sid)            
        else:
            pass

    #basic play actions

    def checkCardAvailable(self, player, card):
        #check available cards during play phase            
        if card.type == c.ITEM:

            if player.itemPlayed >= player.itemLimit:
                return False

            elif isinstance(card, c.Shield):
                return True if any([isinstance(unit, c.Legionary) for unit in player.units]) else False
            
            elif isinstance(card, c.Horse):
                return True if any([isinstance(unit, c.Cavalry) for unit in player.units]) else False

            elif isinstance(card, c.Arrows):
                return True if any([isinstance(unit, c.Archery) for unit in player.units]) else False
            
            elif isinstance(card, c.Ration):
                return True

            elif isinstance(card, c.Aquilifer):
                return True if len(player.units) else False

        elif card.type == c.UNIT:
            card.avaiable = False if len(player.units) >= 3 else True

    
        elif card.type == c.MILITARY:

            if isinstance(card, c.Testudo):
                return False

            elif isinstance(card, c.Camp):
                return True if len(player.units) else False
            
            elif isinstance(card, c.Barbarian_Invasion):
                return True if any([unit.ap == 1 for unit in player.opp.units]) else False 

            return True

        else: #remaining card type: political
            if self.politicalPlayed >= self.politicalLimit:
                return False

            elif isinstance(card, c.Urban_Construction):
                return True if len(self.hand) >= 2 else False

            elif isinstance(card, c.Veto):
                return False

            return True

    def Handle(self, player, e):
        match e:
            case "preturnDone":
                self.drawphase(player)
            case "drawPhaseDone":
                self.playphase(player)
            case "playPhaseDone":
                self.discardphase(player)
            case "discardPhaseDone":
                self.battlephase(player)
            case "battlePhaseDone":
                self.postturn(player)
            case "postPhaseDone":
                self.preturn(player.opp)

    def preturn(self, player):
        pass

    def drawphase(self, player):
        self.drawCard(player, 2)
        self.Handle(player, )

   
    def playphaseListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        #input -1 if player wishes to end playphase
        n = data["n"]
        if n < 0:
            self.playphaseOngoing = False
        else:
            card = character.hand[n]
            del character.hand[n]
            #show opponent which card were played
            self.room.send("opponentCard", {"n":len(character.hand)}, character.opp.sid)
            self.room.send("opponentPlayCard", {"card":card.toJson()}, character.opp.sid)
            
            self.playCard(character, card)
        self.playing.set()

    def playphase(self, player):
        while self.playphaseOngoing:
            self.playing.clear()
            n = []
            #check playable cards
            for card in player.hand:
                if self.checkCardAvailable(player, card):
                    n.append(card)
            if not len(n):
                break
            self.room.send("playInput", {"n": n}, player.sid)
            self.playing.wait()
        self.playphaseOngoing = True 
        self.Handle(player)


    def discardphase(self, player):
        if len(player.hand) > player.handLimit:
            self.discardCardRequest(player, len(player.hand) - player.handLimit)
        self.Handle(player)


    def battlephase(self, player):
        self.Handle(player)
        pass

    def postturn(self, player):
        self.Handle(player)
        self.resetCount()


if __name__ == "__main__":
    g = GameManager()
    print([c.name for c in g.generateCharacters(Characters.ENEMY)])