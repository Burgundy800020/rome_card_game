from random import shuffle, choices
import flask

if __package__ is None or __package__ == "":
    import Card as c, Characters, Unit as u
    import Card, Characters
else:
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

    def showCard(self, player, card:c.Card, label):
        json_card = card.toJson
        self.room.send("showCard", {"card":json_card, "player" : player.name, "label" : label}, player.sid)
        self.room.send("showCard", {"card":json_card, "player" : player.name, "label" : label}, player.opp.sid)
    
    #Basic card actions
    def drawCard(self, character:Characters.Player, n):
        #modify player's hand in backend
        for i in range(n):
            card = choices(self.deck, weights=self.weights, k=1).pop()()
            character.hand.append(card)
        #update hand to both players
        self.updateHand(character)

    def discardCardListen(self, data, next_event=None):
        sid = flask.request.sid
        character = self.room.clients[sid]
        #remove cards from player's hand
        n = data["n"]
        n.sort(reverse=True)
        for i in n:
            self.showCard(character, character.hand[i], "Discard")
            del character.hand[i] 
        #update hand to both players
        self.updateHand(character)
        if next_event is not None:
            self.Handle(character, next_event)
        
    
    def discardCard(self, character:Characters.Player, n, next_event):
        self.room.send("discardInput", {"n": n}, character.sid)
    
    def reveal(self, character:Characters.Player):
        card = choices(self.deck, weights=self.weights, k=1).pop()
        self.showCard(character, card, "Reveal")
        return card.numeral

    def updateHand(self, player:Characters.Player):
        hand = player.handToJson()
        self.room.send("setCardState", {"playerCards":hand}, player.sid)
        self.room.send("setCardState", {"opponentCards":len(hand)}, player.opp.sid)

    #basic hp actions
    def heal(self, character:Characters.Player, n):
        character.hp = min(character.hp + n, 10)
        self.room.send("playerHp", {"hp": character.hp}, character.sid)
        self.room.send("opponentHp", {"hp":character.hp}, character.opp.sid)
    
    #deal n damage to character
    #The damage is decisive if it results from a Legionary or Cavalry attack
    def dealDamage(self, character:Characters.Player, n, decisive=False):
        if character.name == "Mithridates":
            if character.immune: 
                n -= 1
            else:
                character.immune = True

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
        i = data["i"]
        card = data["card"] #the military card that the opponent played
        
        if i >= 0:
            #show played card
            del character.hand[i]
            self.updateHand(character)
            self.Handle(character.opp, "drawPhaseDone")
        else:
            self.playMilitary(character.opp, c.Card(name = card))
    
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
        self.updateUnits(character)
        self.Handle(character, "drawPhaseDone")
        
    def vetoListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        i = data["i"]
        card = data["card"] #the military card that the opponent played
        
        if i >= 0:
            #show played card
            del character.hand[i]
            self.updateHand(character)
            self.Handle(character.opp, "drawPhaseDone")
        else:
            self.playPolitical(character.opp, c.Card(name = card))

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
            if self.reveal(player) %3!=0:
                player.opp.sieged=True
                #show player sieged
            
        elif card.name == "onager":
            if self.reveal(player) %3!=0:
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
            if self.reveal(player) %3!=0:
                player.opp.panemed = True
                #show player panemd

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
            if player.name == 'Pompeius':
                self.drawCard(player, 1)
            n = []
            for i in range(len(player.opp.hand)):
                if player.opp.hand[i].name=="testudo":
                    n.append(i)
            if(len(n)):
                self.room.sent("testudoInput", {"n" : n, "card" : card.name}, player.opp.sid)
                return
            self.playMilitary(player, card)       

        else:
            player.PoliticalPlayed += 1
            if player.name == 'Caesar':
                #show quote
                self.drawCard(player, 1)
            
            elif player.name == 'Octavius' and player.awaken:
                #show quote
                self.drawCard(player, 1)

            if isinstance(card, c.Senatus_Cousultum_Ultimum):
                self.playPolitical(player, card)
                return
            for i in range(len(player.opp.hand)):
                if player.opp.hand[i].name=="veto":
                    n.append(i)
            if(len(n)):
                self.room.sent("vetoInput", {"n" : n, "card" : card.name}, player.opp.sid)
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
        elif e == "battleDiscardDone":
            self.defend(player)

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
            for i in range(len(character.units)):
                if isinstance(character.units[i], u.Celtic) or character.units[i].type == u.AUX:
                    cardNum += 1
                    self.remove(character, i ,1)
            self.drawCard(character, cardNum)
        self.Handle(character, "preTurnDone")
        
    #-------------------------------------------------------------------------------------

    def preturn(self, player):
        if player.name == "Marius":
            if len(player.hand) <= 2:
                self.drawCard(player, 3)
                self.heal(player, 1)         
                self.Handle(player, "postTurnDone")
                return

        elif player.name == "Cicero":
            healingHP=0
            for i in range(len(player.units)):
                if player.units[i].type == u.MAIN: 
                    if self.reveal(player) %3!=0:
                        healingHP+=1
            if healingHP!=0:
                self.heal(player.sid, healingHP)
            
        elif player.name == "Octavius" and not player.awaken:
            if player.hp<=4:
                self.drawCard(player,1)
                self.heal(player, 1)
                player.PoliticalLimit = 100
                player.awaken = True

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

    def creditorListen(self, data):
        sid = flask.request.sid
        player = self.room.clients[sid]
        i = data["i"]
        player.opp.hand.append(player.hand[i])
        del player.hand[i]
        self.updateHand(player)
        self.updateHand(player.opp)
        self.drawCard(player.opp, 1)
        self.Handle(player.opp, 'drawPhaseDone')

    def drawphase(self, player:Characters.Player):
        if not player.sieged:
            if player.name == 'Octavius' and player.awaken:
                self.drawCard(player, 3)
            elif player.name == 'Crassus':
                if len(player.opp.hand):
                    self.room.send("creditorInput", {}, player.sid)
                    return
                self.drawCard(player, 1)
                    
            else:
                self.drawCard(player, 2)
        self.Handle(player, "drawPhaseDone")

    def playphaseListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        #input -1 if player wishes to end playphase
        i = data["n"]
        if i >= 0:
            card = character.hand[i]
            self.showCard(character, card, "Play")
            del character.hand[i]
            #show opponent which card were played
            self.updateHand(character)
            self.playCard(character, card)
        else:
            self.Handle(character, "playPhaseDone")

    def playphase(self, player:Characters.Player):
        if player.panemed:
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
        else:
            self.Handle(player, "discardPhaseDone")

    def diplomatListen(self, data):
        sid = flask.request.sid
        player = self.room.clients[sid]
        i = data["i"]
        if i:
            del player.opp.units[i]
            self.updateUnits(player.opp)
            self.Handle(player, "battlePhaseDone")
        else:
            self.attackDamage(player.opp)

    def elephantListen(self, data):
        sid = flask.request.sid
        player = self.room.clients[sid]
        i = data["i"]
        if i:
            del player.opp.units[i]
            self.updateUnits(player.opp)        
        self.attackDamage(player.opp)

    def attackFailure(self, player:Characters.Player):
        self.remove(player, player.main, 1)
        if(player.aux >= 0):
            self.remove(player, player.aux, 1)
        self.Handle(player.opp, "battlePhaseDone")
        

    def attackSuccess(self, player:Characters.Player):
        main_u = player.units[player.main]
        n = []
        if isinstance(main_u, u.Archery):
            self.dp -= 1
        if player.name == 'Sulla':
            for i in range(len(player.opp.units)):
                if player.opp.units[i].ap <= player.dp:
                    n.append(i)
            self.room.send("diplomatInput", {"n":n}, player.sid)
            return
        elif isinstance(main_u, u.Elephant):
            for i in range(len(player.opp.units)):
                if player.opp.units[i].ap <= 1:
                    n.append(i)
            self.room.send("elephantInput", {"n":n}, player.sid)
            return
        elif isinstance(main_u, u.Celtic):
            self.heal(player, 1)
        self.attackDamage(player.opp)
        
    def attackDamage(self, player:Characters.Player):        
        self.dealDamage(player, player.opp.dp)

        if any([isinstance(unit, c.Elephant) for unit in player.units]) and isinstance(player.opp.units[player.opp.main], u.Archery):
            for i in range(len(player.units)):
                self.remove(player, i, 1)
        
        self.remove(player.opp, player.opp.main, 1)
        if player.opp.aux >= 0:
            self.remove(player.opp, player.opp.aux, 1)

        elif isinstance(player, Characters.Cicero) and len(player.opp.hand) > 0:
            if self.reveal(player) % 3 == 0:
                self.discardCard(player.opp, min(2, len(player.opp.hand)), "battlePhaseDone")
                return
        self.Handle(player.opp, "battlePhaseDone")
    
    def defendListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        def_n = data['def']
        n = data['n']
        n.sort(reverse=True)
        for i in n:
            self.showCard(character, character.hand[i], "Defend")
            del character.hand[i] 
        self.updateHand(character)
        if len(n) < def_n:
            self.attackSuccess(character.opp)
        else:
            self.attackFailure(character.opp, "battlePhaseDone")


    def defend(self, player, def_n):
        n = []
        for i in range(len(player.hand)):
            if player.hand[i].name == 'shield':
                n.append(i)
        self.room.send("defend", {"n" : n, "def" : def_n}, player.sid)
    
    def battleDiscardListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        def_n = data['def']
        n = data["n"]
        n.sort(reverse=True)
        for i in n:
            del self.hand[i] 
        self.updateHand(character)
        self.defend(character, def_n)

    def attack(self, player):
        main_u = player.units[player.main]
        if player.name == 'Surena' and len(player.opp.hand) > len(player.hand):
            player.dp += 1

        elif player.name == 'Caesar':
            if self.reveal(player) % 2 == 0:
                player.dp += 1


        elif player.name == 'Spartacus' and player.revolted:    
            player.dp += 1

        if player.opp.name == 'Caesar' and len(player.units) > len(player.opp.units):
            self.drawCard(player.opp, 1)

        if isinstance(main_u, u.Archery):
            if isinstance(main_u, u.Mounted_Archer) and player.opp.hp >= 6:
                player.dp += 1
            self.attackSuccess(player)

        else:
            def_n = 1
            dis_n = 0
            if isinstance(main_u, u.Cavalry) and player.opp.hp >= 6:
                player.dp += 1
                
            if player.aux >= 0:
                aux_u = player.units[player.aux]
                def_n += isinstance(aux_u, u.Velite)
                dis_n += isinstance(aux_u, u.Slinger)
            if isinstance(main_u, u.Gladiator):
                def_n += 1
            if isinstance(main_u, u.Phalanx):
                dis_n += 1
            if isinstance(main_u, u.Gladiator):
                def_n += 1
            if dis_n:
                self.room.send("battleDiscard", {"dis" : dis_n, 'def' : def_n}, player.opp.sid)
                return
            self.defend(player.opp, def_n)

        self.Handle(player, "battlePhaseDone")

    def auxListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        character.aux = data["i"]
        self.attack(character)
                
    #main, aux are the indices of the chosen units
    def battlephaseListen(self, data):
        sid = flask.request.sid
        character = self.room.clients[sid]
        #input -1 if player does not with to attack
        main = data["i"]
        if main >= 0:
            #select auxiliary unit
            character.main = main
            if isinstance(character.units[main], u.Legionary):
                n = []
                for index in range(len(character.units)):
                    if character.units[index].type == u.AUX and character.units[index].available:
                        n.append(index)
                if len(n):
                    self.room.send("auxInput", {"n": n}, character.sid)
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

    def postturn(self, player : Characters.Player):
        if player.name == "Sulla":
            #insert character logic
            pass

        self.Handle(player, "PostTurnDone")
    
    

if __name__ == "__main__":
    g = GameManager()
    print([c.name for c in g.generateCharacters(Characters.ENEMY)])