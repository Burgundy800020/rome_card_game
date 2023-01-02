from random import shuffle, choices
import flask, flask_socketio

#import Card as c, Characters, Unit as u
#import Card, Characters
from . import Card as c
from . import Characters
from . import Unit as u


class GameManager:
    def __init__(self, room, socketIO):
        self.room = room
        self.socketIO = socketIO
        self.remRomans = Characters.characterList.copy(); shuffle(self.remRomans)
        self.deck = [c.Shield, c.Horse, c.Arrows]
        self.weights = [1,1,1]
        self.players = []
        self.currentPlayer = False

        #listen to channels
        self.socketIO.on(f"{self.room.id}/discardCard")(self.discardCardListen)
        self.socketIO.on(f"{self.room.id}/playphase")(self.playphaseListen)

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
        self.updateHand(character)

    def discardCardListen(self, data, next_event=None):
        sid = flask.request.sid
        character = self.room.clients[sid]
        #remove cards from player's hand
        n = data["n"]
        n.sort(reverse=True)
        for i in n:
            del self.hand[i] 
        #update hand to both players
        self.updateHand(character)
        if next_event is not None:
            self.Handle(character, next_event)
        
    
    def discardCard(self, character:Characters.Player, n, next_event):
        self.room.send("discardInput", {"n": n}, character.sid)
    
    def reveal(self, character:Characters.Player):
        card = choices(self.deck, weights=self.weights, k=1).pop()()
        self.room.send("revealCard", {"card":card}, character.sid)
        self.room.send("revealCard", {"card":card}, character.opp.sid)
        return card

    def updateHand(self, player:Characters.Player):
        hand = player.handToJson()
        self.room.send("playerCard", {"hand":hand}, player.sid)
        self.room.send("opponentCard", {"n":len(hand)}, player.opp.sid)

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
        
        if isinstance(character, Characters.Cicero) and len(character.opp.hand) >= 2:
            card = self.reveal(character)
            if card.numeral % 3 == 0:
                self.discardCard(character.opp, 2, "")

    #basic unit actions
    def restore(self, player:Characters.Player, i, n):
        unit = player.units[i]
        player.unit.ap = min(unit.ap + n, unit.maxAp)
        self.updateUnits(player)

    def remove(self, player:Characters.Player, i, n):
        unit = player.units[i]
        if unit.ap > n:
            unit.ap -= n
        else:
            del unit
        self.updateUnits(player)

    def updateUnits(self, player:Characters.Player):
        units = player.unitsToJson()
        self.room.send("playerUnits", {"units": units}, player.sid)
        self.room.send("opponentUnits", {"units" : units}, player.opp.sid)

#listen to playCard
#--------------------------------------------------------------------------------------------        
    def testudoListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        n = data["n"]
        card = data["card"] #the military card that the opponent played
        if n == 1:
            self.Handle(character.opp, "drawPhaseDone")
        else:
            self.playMilitary(character.opp, card)
    
    def boosterListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        i = data["i"]
        self.restore(character, i, 1)
        self.Handle(character, "drawPhaseDone")
    
    def aquiliferListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        i = data["i"]
        character.units[i].available = True
        self.updateUnits(character)
        self.Handle(character, "drawPhaseDone")

    def barbarianListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        i = data["i"]
        del character.opp.units[i]
        self.updateUnits(character.opp)
        self.Handle(character, "drawPhaseDone")

    def campListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        i = data["i"]
        character.units[i].available = False
        self.restore(character, i, 1)
        self.Handle(character, "drawPhaseDone")
        
    def vetoListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        n = data["n"]
        card = data["card"] #the military card that the opponent played
        if n == 1:
            self.Handle(character.opp, "drawPhaseDone")
        else:
            self.playPolitical(character.opp, card)

    def urbanListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        self.heal(character, 3)
        self.Handle(character, "drawPhaseDone")

    def senatusListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        n = data["n"]
        #0 : discard hand. 1: lose 3 hp
        if n == 0:
            character.hand.clear()
            self.updateHand(character)
        else:
            self.dealDamage(character, 3)
        self.Handle(character, "drawPhaseDone")
#-----------------------------------------------------------------------------
    def playMilitary(self, player:Characters.Player, card : c.Card):
        n = []
        if card.name == "barbarian_invasion":
            for i in range(len(player.opp.units)):
                if player.opp.units[i].ap == 1:
                    n.append(i)
            self.room.send("barbarianInput", {"n": n}, player.sid)
            return

        elif card.name == "camp":
            for i in range(len(player.opp.units)):
                n.append(i)
            self.room.send("campInput", {"n": n}, player.sid)
            return

        elif card.name == "siege":
            revealed = self.reveal(player)
            if revealed.numeral%3!=0:
                player.opp.sieged=True
            
        elif card.name == "onager":
            revealed = self.reveal(player)
            if revealed.numeral%3!=0:
                self.dealDamage(player.opp, 2)
            
        elif card.name == "reinforcement":
            self.drawCard(player, 2)
                
        self.Handle(player, "drawPhaseDone")

    def playPolitical(self, player:Characters.Player, card:c.Card):
        
        if card.name == "senatus_consultum_ultimum":
            self.room.send("senatusInput",{}, player.opp.sid)
            return

        elif card.name == "land_redistribution":
            player.hand.clear()
            self.drawCard(player, len(player.opp.hand))

        elif card.name ==  "panem_et_circenses":
            revealed = self.reveal(player)
            if revealed.numeral %3!=0:
                player.opp.panemed = True

        elif card.name == "urban_construction":
            self.discardCard(player, 1, "urbanConstruction")
            return     

        self.Handle(player, "drawPhaseDone")
        
    def playCard(self, player: Characters.Player, card: c.Card):
        if card.type == c.ITEM:
            player.itemPlayed += 1
            n = []
            
            if card.name == "ration":
                self.heal(player, 2)
            elif card.name == "shield":
                for i in range(len(player.units)):
                    if isinstance(player.units[i], u.Legionary):
                        n.append(i)
                self.room.send("boosterInput", {"n": n}, player.sid)
            elif card.name == "arrow":
                for i in range(len(player.units)):
                    if isinstance(player.units[i], u.Archery):
                        n.append(i)
                self.room.send("boosterInput", {"n": n}, player.sid)
            elif card.name == "horse":
                for i in range(len(player.units)):
                    if isinstance(player.units[i], u.Cavalry):
                        n.append(i)
                self.room.send("boosterInput", {"n": n}, player.sid)
            elif card.name == "aquilifer":
                for i in range(len(player.units)):
                    if not player.units[i].available:
                        n.append(i)
                self.room.send("aquiliferInput", {"n": n}, player.sid)  

        elif card.type == c.UNIT:
            
            if card.name == "legionary":
                if player.name == "Marius":
                    unit = u.Legionary(ap = 3, avail=True)
                elif player.name == "Spartacus":
                    unit = u.Gladiator()
                elif player.name == "Vercingetorix":
                    unit = u.Celtic()
                elif player.name == "Mithridates":
                    unit = u.Phalanx()  
                else:
                    unit = u.Legionary()
            if card.name == "cavalry":
                if player.name == "Hannibal":
                    unit = u.Elephant()
                else:
                    unit = u.Cavalry()  
            if card.name == "archery":
                if player.name == "Surena":
                    unit = u.Mounted_Archer()
                else:
                    unit = u.Archery()  
            if card.name == "velite":
                unit = u.Velite()
                if isinstance(player, Characters.Marius):
                    unit.available = True
                    unit.ap = 2
            if card.name == "slinger":
                unit = u.Slinger()
                if isinstance(player, Characters.Marius):
                    unit.available = True
                    unit.ap = 2                    
            player.units.append(unit)
            self.updateUnits(player)

        elif card.type == c.MILITARY:
            if isinstance(player, Characters.Pompeius):
                self.drawCard(player, 1)

            for card in player.opp.card:
                if card.name=="testudo":
                    self.room.send("testudoInput", player.opp.sid)
                    return
            self.playMilitary(player, card)       

        else:
            player.PoliticalPlayed += 1
            if isinstance(player, Characters.Caesar):
                self.drawCard(player, 1)

            if isinstance(card, c.Senatus_Cousultum_Ultimum):
                self.playPolitical(player, card)
                return
            for card in player.opp.card:
                if card.name=="veto":
                    self.room.send("vetoInput", player.opp.sid)
                    return
            self.playPolitical(player, card)

    def checkCardAvailable(self, player:Characters.Player, card:c.Card):
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
            return False if len(player.units) >= 3 else True

    
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
        if e == "preTurnDone":
            self.drawphase(player)
        elif e == "drawPhaseDone":
            self.playphase(player)
        elif e == "playPhaseDone":
            self.discardphase(player)
        elif e == "discardPhaseDone":
            self.battlephase(player)
        elif e == "battlePhaseDone":
            self.postturn(player)
        elif e == "postTurnDone":
            self.reset(player)
        elif e == "resetDone":
            self.preturn(player.opp)
        elif e == "urbanConstruction":
            self.urbanListen(player)

    def reset(self, player:Characters.Player):
        for unit in player.units:
            unit.available = True
        self.updateUnits(player)
        player.resetCount()
        self.Handle(player, "resetDone")
        
    #preturn abilities
    #-------------------------------------------------------------------------------------

    def tribalListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        n = data["n"]
        if n == 1:
            cardNum = 0
            for unit in character.units:
                if isinstance(unit, u.Celtic) or unit.type == u.AUX:
                    cardNum += 1
                    self.remove(u ,1)
            self.drawCard(character, cardNum)
        self.Handle(character, "preTurnDone")
        
    #-------------------------------------------------------------------------------------

    def preturn(self, player):
        if player.name == "Caius Marius":
            if len(player.hand) <= 2:
                self.drawCard(player, 3)
                self.heal(player, 1)         
                self.Handle(player, "postTurnDone")
                return

        elif player.name == "Cicero":
            healingHP=0
            for i in range(len(player.units)):
                if player.units[i].type == u.MAIN: 
                    card = self.reveal(player)
                    if(card.numeral%3==0):
                        healingHP+=1
            if healingHP!=0:
                self.heal(player.sid, healingHP)
            
        elif player.name == "Octavius":
            if player.hp<=4:
                self.drawCard(player,1)
                self.heal(player, 1)

        elif player.name == "Vercingetorix":
            n = []
            for i in range(len(player.units)):
                if isinstance(player.units[i], u.Celtic) or player.units[i].type == u.AUX:
                    n.append(i)
            if len(n):
                self.room.send("tribalInput", {"n":n}, player.sid)
                return
                
        elif player.name == "Spartacus":
            pass
            #insert character logic
                    
        self.Handle(player, "preTurnDone")


    async def drawphase(self, player:Characters.Player):
        if not player.sieged:
            await self.drawCard(player, 2)
        await self.Handle(player, "drawPhaseDone")

    def playphaseListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        #input -1 if player wishes to end playphase
        n = data["n"]
        if n >= 0:
            card = character.hand[n]
            del character.hand[n]
            #show opponent which card were played
            self.room.send("opponentCard", {"n":len(character.hand)}, character.opp.sid)
            self.room.send("opponentPlayCard", {"card":card.toJson()}, character.opp.sid)
            self.playCard(character, card)
        else:
            self.Handle(character, "playPhaseDone")

    def playphase(self, player):
        if player.panemd:
            self.Handle(player, "battlePhaseDone")
            return

        n = []
        #check playable cards
        for i in range(len(player.hand)):
            if self.checkCardAvailable(player, player.hand[i]):
                n.append(i)
        if len(n):
            self.room.send("playInput", {"n": n}, player.sid)
        else:
            self.Handle(player, "playPhaseDone")
        

    def discardphase(self, player):
        if len(player.hand) > player.handLimit:
            self.discardCard(player, len(player.hand) - player.handLimit, "discardPhaseDone")

    def attack(self, player, main, aux=-1):
        #todo: implement case-by-case attack logic
        self.Handle(player, "battlePhaseDone")

    def auxListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        main = data["main"]
        aux = data["aux"]
        self.attack(character, main, aux=aux)
                
    #main, aux are the indices of the chosen units
    def battlephaseListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        #input -1 if player does not with to attack
        main = data["main"]
        if main >= 0:
            #select auxiliary unit
            if isinstance(character.units[main], u.Legionary):
                n = []
                for index in range(len(character.units)):
                    if character.units[index].type == u.AUX and character.units[index].available:
                        n.append(index)
                if len(n):
                    self.room.send("auxInput", {"n": n, "main" : main}, character.sid)
                else:
                    self.attack(character, main)
            else:
                self.attack(character, main)
        else:
            self.Handle(character, "battlePhaseDone")

    def battlephase(self, player):
        n = []
        for i in range(len(player.units)):
            if player.units[i].type == u.MAIN and player.units[i].available:
                n.append(i)
        if len(n):
            self.room.send("battleInput", {"n": n}, player.sid)
        else:
            self.Handle(player, "battlePhaseDone")

    def postturn(self, player):
        if player.name == "Sulla":
            #insert character logic
            pass

        self.Handle(player)
        self.resetCount()

if __name__ == "__main__":
    g = GameManager()
    print([c.name for c in g.generateCharacters(Characters.ENEMY)])