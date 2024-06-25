from random import shuffle, choices, randint
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
        self.deck = [c.Shield, c.Horse, c.Arrows, c.Ration, c.Aquilifer, c.Legionary, c.Archery, c.Cavalry,
                     c.Velite, c.Slinger,
                     c.Camp, c.Reinforcements, c.Testudo, c.Barbarian_Invasion,c.Siege, c.Onager,
                     c.Land_Redistribution, c.Veto, c.Urban_Construction, c.Panem_Et_Circenses, c.Senatus_Cousultum_Ultimum]
        self.weights = [card.frq for card in self.deck]
        self.players = []
        self.currentPlayer = False

        #listen to channels
        self.socketIO.on(f"{self.room.id}/playListen")(self.playListen)
        self.socketIO.on(f"{self.room.id}/deployListen")(self.deployListen)
        self.socketIO.on(f"{self.room.id}/destroyListen")(self.destroyListen)
        self.socketIO.on(f"{self.room.id}/chooseListen")(self.chooseListen)


    def addPlayer(self, character, sid=""):
        player = Characters.characterList[Characters.nameList.index(character)](self, sid=sid)
        self.players.append(player)
        return player

    def generateCharacters(self):
        #take two first characters (and remove them) from list
        characterChoices = self.remRomans[:2]
        self.remRomans = self.remRomans[2:]
        return [character.name for character in characterChoices]
    
    def playInput(self, player:Characters.Player, n, event, choices = None):
        player.play_event = event
        player.choose_event = event
        self.room.send("playInput", {"n": n, "event" : event, "choices" : choices}, player.sid)

    def deployInput(self, player:Characters.Player, n, event, choices = None):
        player.deploy_event = event
        player.choose_event = event
        self.room.send("deployInput", {"n": n, "event" : event, "choices" : choices}, player.sid)
    
    def destroyInput(self, player:Characters.Player, n, event, choices = None):
        player.destroy_event = event
        player.choose_event = event
        self.room.send("destroyInput", {"n": n, "event" : event, "choices" : choices}, player.sid)

    def addDialogue(self, text):
        for i in (0, 1):
            self.room.send("addDialogue", {"text":text}, self.players[i].sid)

    def showQuote(self, player:Characters.Player, i):
        self.addDialogue(f"{player.name} used ability <<{player.abilities[i]}>>")
        text = f"{player.quotes[i][randint(0, len(player.quotes[i])-1)]}"
        self.room.send("addQuote", {"playerQuote":text}, player.sid)
        self.room.send("addQuote", {"opponentQuote":text}, player.opp.sid)

    #Basic card actions
    def drawCard(self, character:Characters.Player, n):
        #modify player's hand in backend
        for i in range(n):
            card = choices(self.deck, weights=self.weights, k=1).pop()()
            character.hand.append(card)
        #update hand to both players
        self.updateHand(character)

    def discardCardListen(self, character:Characters.Player, i):      
        #self.showCard(character, character.hand[i], "Discard")
        self.addDialogue(f"{character.name} discarded [{character.hand[i].name}]")
        del character.hand[i] 
        self.updateHand(character)
        character.discard -= 1
        if character.discard > 0:
            self.discardCard(character)
        else:
            self.Handle(character, character.discard_event)
    
    def discardCard(self, character:Characters.Player):
        self.playInput(character, [i for i in range(len(character.hand))], Characters.DISCARD)
    
    def reveal(self, player:Characters.Player):
        num = randint(1, 6)
        self.addDialogue(f"{player.name} rolled {num}")
        return num

    def updateHand(self, player:Characters.Player):
        hand = player.handToJson()
        self.room.send("updateHand", {"playerCards":hand}, player.sid)
        self.room.send("updateHand", {"opponentCards":len(hand)}, player.opp.sid)

    def updateStates(self, player:Characters.Player, state, on):
        player.states[state] = on
        self.room.send("updateStates", {"player":player.states}, player.sid)
        self.room.send("updateStates", {"opponent":player.states}, player.opp.sid)

    #basic hp actions
    def heal(self, character:Characters.Player, n):
        character.hp = min(character.hp + n, 10)
        self.room.send("updateHp", {"playerHp": character.hp}, character.sid)
        self.room.send("updateHp", {"opponentHp":character.hp}, character.opp.sid)
    
    #deal n damage to character
    #The damage is decisive if it results from a Legionary or Cavalry attack
    def dealDamage(self, character:Characters.Player, n):
        if character.name == "Mithridates":
            if character.immune: 
                n -= 1
            else:
                character.immune = True

        
        character.hp = max(character.hp-n, 0)
        
        #update hp to both players
        self.room.send("updateHp", {"playerHp": character.hp}, character.sid)
        self.room.send("updateHp", {"opponentHp":character.hp}, character.opp.sid) 

        if not character.hp:
            self.room.send("gameOver", {}, character.sid)
            self.room.send("gameOver", {}, character.opp.sid)
        
    #basic unit actions
    def restore(self, player:Characters.Player, i, n):
        unit:u.Unit = player.units[i]
        unit.ap = min(unit.ap + n, unit.maxAp)
        self.updateUnits(player)

    def remove(self, player:Characters.Player, i, n):
        unit:u.Unit = player.units[i]
        if unit.ap > n:
            unit.ap -= n
        else:
            del player.units[i]
        self.updateUnits(player)

    def updateUnits(self, player:Characters.Player):
        units = player.unitsToJson()
        self.room.send("updateUnits", {"playerUnits": units}, player.sid)
        self.room.send("updateUnits", {"opponentUnits" : units}, player.opp.sid)

#listen to playCard
#--------------------------------------------------------------------------------------------        
    
    def boosterListen(self, character, i):
        self.restore(character, i, 1)
        self.Handle(character, "drawPhaseDone")
    
    def aquiliferListen(self, character, i):
        character.units[i].available = True
        self.updateUnits(character)
        self.Handle(character, "drawPhaseDone")

    def urbanListen(self, character):
        self.heal(character, 3)
        self.Handle(character, "drawPhaseDone")

    def senatusListen(self, character:Characters.Player, i):
        if i == 0:
            character.units.clear()
            self.addDialogue(f"{character.name} obeyed to the Senate's decree and handed over their legions")
            self.updateUnits(character)
        else:
            self.addDialogue(f"{character.name} disobeyed to the Senate's decree and was declared enemy of the State")
            self.updateStates(character, 'proscriptio', True)
        self.Handle(character.opp, "drawPhaseDone")
#-----------------------------------------------------------------------------
    def playMilitary(self, player:Characters.Player, card : c.Card):
        player.resetCard()
        n = []
        if isinstance(card, c.Barbarian_Invasion):
            for i in range(len(player.opp.units)):
                if player.opp.units[i].ap == 1:
                    n.append(i)
            self.destroyInput(player, n, Characters.BARBARIAN)
            return

        elif isinstance(card, c.Camp):
            for i in range(len(player.units)):
                n.append(i)
            self.deployInput(player, n, Characters.CAMP)
            return

        elif isinstance(card, c.Siege):
            if self.reveal(player) %3!=0:
                self.updateStates(player.opp, 'sieged', True)
                
        elif isinstance(card, c.Onager):
            if self.reveal(player) %3!=0:
                self.dealDamage(player.opp, 2)
            
        elif isinstance(card, c.Reinforcements):
            self.drawCard(player, 2)
                
        self.Handle(player, "drawPhaseDone")

    def playPolitical(self, player:Characters.Player, card:c.Card):
        player.resetCard()
        if isinstance(card, c.Senatus_Cousultum_Ultimum):
            self.destroyInput(player.opp, [], Characters.CONSULTUM, ['hand over legions', 'ignore'])
            return

        elif isinstance(card, c.Land_Redistribution):
            player.hand.clear()
            self.drawCard(player, len(player.opp.hand))

        elif isinstance(card, c.Panem_Et_Circenses):
            if self.reveal(player) %3!=0:
                self.updateStates(player.opp, 'panem', True)

        elif isinstance(card, c.Urban_Construction):
            player.discard = 1
            player.discard_event = "urbanConstruction"
            self.discardCard(player)
            return     

        self.Handle(player, "drawPhaseDone")
        
    def playCard(self, player: Characters.Player, card: c.Card):
        if card.type == c.ITEM:
            self.addDialogue(f"{player.name} played [{card.name}]")               
            player.itemPlayed += 1
            n = []
            if isinstance(card, c.Aquilifer):
                for i in range(len(player.units)):
                    if not player.units[i].available:
                        n.append(i)
                self.deployInput(player, n, Characters.AQUILIFER)
                return
            if isinstance(card, c.Ration):
                self.heal(player, 2)
                self.Handle(player, "drawPhaseDone")
                return
            elif isinstance(card, c.Shield):
                for i in range(len(player.units)):
                    if isinstance(player.units[i], u.Legionary):
                        n.append(i)
            elif isinstance(card, c.Arrows):
                for i in range(len(player.units)):
                    if isinstance(player.units[i], u.Archery):
                        n.append(i)
            elif isinstance(card, c.Horse):
                for i in range(len(player.units)):
                    if isinstance(player.units[i], u.Cavalry):
                        n.append(i)
            self.deployInput(player, n, Characters.BOOST)
            
        elif card.type == c.UNIT:
            unit = u.Legionary()
            if isinstance(card, c.Legionary):
                if isinstance(player, Characters.Marius):
                    self.showQuote(player, 0)
                    unit = u.Legionary(ap = 3, avail=True)
                elif isinstance(player, Characters.Spartacus):
                    unit = u.Gladiator()
                elif player.name == "Vercingetorix":
                    unit = u.Celtic()
                elif player.name == "Mithridates":
                    unit = u.Phalanx()  
                else:
                    unit = u.Legionary()
            elif isinstance(card, c.Cavalry):
                if player.name == "Hannibal":
                    unit = u.Elephant()
                else:
                    unit = u.Cavalry()  
            elif isinstance(card, c.Archery):
                if player.name == "Surena":
                    unit = u.Mounted_Archer()
                else:
                    unit = u.Archery()  
            elif isinstance(card, c.Velite):
                unit = u.Velite()
                if isinstance(player, Characters.Marius):
                    self.showQuote(player, 0)
                    unit.available = True
                    unit.ap = 2
            elif isinstance(card, c.Slinger):
                unit = u.Slinger()
                if isinstance(player, Characters.Marius):
                    self.showQuote(player, 0)
                    unit.available = True
                    unit.ap = 2     
            self.addDialogue(f"{player.name} raised a new <{unit.name}> unit")               
            player.units.append(unit)
            self.updateUnits(player)
            self.Handle(player, "drawPhaseDone")

        elif card.type == c.MILITARY:
            self.addDialogue(f"{player.name} played [{card.name}]")               
            player.military = card
            if player.name == 'Pompeius':
                self.showQuote(player, 0)
                self.drawCard(player, 1)
            n = []
            for i in range(len(player.opp.hand)):
                if player.opp.hand[i].name=="testudo":
                    n.append(i)
            if len(n):
                self.playInput(player.opp, n, Characters.TESTUDO, choices=['cancel'])
                return
            self.playMilitary(player, card)
        else:
            self.addDialogue(f"{player.name} played [{card.name}]")               
            player.PoliticalPlayed += 1
            player.political = card
            if player.name == 'Caesar':
                self.showQuote(player, 1)
                self.drawCard(player, 1)
            
            elif player.name == 'Octavius' and player.awaken:
                #show quote
                self.drawCard(player, 1)
            
            if isinstance(card, c.Senatus_Cousultum_Ultimum):
                self.playPolitical(player, card)
                return
            n = []
            for i in range(len(player.opp.hand)):
                if player.opp.hand[i].name=="veto":
                    n.append(i)
            if len(n):
                self.playInput(player.opp, n, Characters.VETO, choices=['cancel'])
                return
            self.playPolitical(player, card)

    def checkCardAvailable(self, player:Characters.Player, card:c.Card):
        #check available cards during play phase            
        if card.type == c.ITEM:
            if player.itemPlayed >= player.itemLimit:
                return False

            elif isinstance(card, c.Shield):
                return True if any([isinstance(unit, u.Legionary) for unit in player.units]) else False
            
            elif isinstance(card, c.Horse):
                return True if any([isinstance(unit, u.Cavalry) for unit in player.units]) else False

            elif isinstance(card, c.Arrows):
                return True if any([isinstance(unit, u.Archery) for unit in player.units]) else False
            
            elif isinstance(card, c.Ration):
                return True

            elif isinstance(card, c.Aquilifer):
                return True if any([not unit.available for unit in player.units]) else False

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
            if player.PoliticalPlayed >= player.PoliticalLimit:
                return False
            if player.states['proscriptio'] and (isinstance(card, c.Senatus_Cousultum_Ultimum) or not isinstance(player, Characters.Caesar)):
                return False

            elif isinstance(card, c.Urban_Construction):
                return True if len(player.hand) >= 2 else False

            elif isinstance(card, c.Veto):
                return False
            return True

    def Handle(self, player:Characters.Player, e):
        if e == "preTurnDone":
            self.drawphase(player)
        elif e == "drawPhaseDone":
            self.playphase(player)
        elif e == "playPhaseDone":
            self.discardphase(player)
        elif e == "discardPhaseDone":
            self.battlephase(player)
        elif e == "battlePhaseDone":
            a = player.main
            b = player.aux
            if a < b:
                a, b = b, a
            if(a >= 0):
                self.remove(player, a, 1)
            if(b >= 0):
                self.remove(player, b, 1)
            self.postturn(player)
        elif e == "postTurnDone":
            self.reset(player)
        elif e == "resetDone":
            self.preturn(player.opp)
        elif e == "urbanConstruction":
            self.urbanListen(player)
        elif e == "battle":
            self.defend(player)
        
    def playListen(self, data):
        sid = flask.request.sid
        character:Characters.Player = self.room.clients[sid]
        event = character.play_event
        character.resetEvent()
        i = data["i"]
        if event == Characters.PLAY: 
            self.playphaseListen(character, i)
            return
        elif event == Characters.DISCARD:
            self.discardCardListen(character, i)
            return 
        elif event == Characters.DEFEND:
            self.defendListen(character, i)
            return
        elif event == Characters.TESTUDO or event == Characters.VETO:                
            del character.hand[i]
            if event == Characters.VETO:
                self.addDialogue(f"{character.name} played [veto]")
            else:
                self.addDialogue(f"{character.name} played [testudo]")
            self.updateHand(character)
            self.Handle(character.opp, 'drawPhaseDone')
        elif event == Characters.CREDITOR:
            card = character.hand[i]
            character.opp.hand.append(card)
            del character.hand[i]
            self.updateHand(character)
            self.updateHand(character.opp)
            self.Handle(character.opp, 'drawPhaseDone')
            


    def deployListen(self, data):
        sid = flask.request.sid
        character:Characters.Player = self.room.clients[sid]
        event = character.deploy_event
        character.resetEvent()
        i = data["i"]
        if event == Characters.DEPLOY_MAIN: 
            self.battlephaseListen(character, i)
            return
        elif event == Characters.DEPLOY_AUX:
            self.auxListen(character, i)
            return 
        elif event == Characters.BOOST:
            self.boosterListen(character, i)
            return
        elif event == Characters.AQUILIFER:
            self.aquiliferListen(character, i)
        elif event == Characters.CAMP:
            character.units[i].available = False
            self.boosterListen(character, i)

    def destroyListen(self, data):
        sid = flask.request.sid
        character:Characters.Player = self.room.clients[sid]
        event = character.destroy_event
        i = data["i"]
        character.resetEvent()
        if event == Characters.BARBARIAN:
            self.remove(character.opp, i, 1)
            self.Handle(character, "drawPhaseDone")
        
        
    def chooseListen(self, data):
        sid = flask.request.sid
        character:Characters.Player = self.room.clients[sid]
        event = character.choose_event
        i = data["i"]
        character.resetEvent()
        if event == Characters.PLAY:
            self.Handle(character, "playPhaseDone")
            return
        elif event == Characters.DEPLOY_MAIN:
            self.Handle(character, "battlePhaseDone")
            return
        elif event == Characters.DEPLOY_AUX:
            self.attack(character)
            return
        elif event == Characters.DEFEND:
            self.attackSuccess(character.opp)
        elif event == Characters.TESTUDO:
            self.playMilitary(character.opp, character.opp.military)
        elif event == Characters.VETO:
            self.playPolitical(character.opp, character.opp.political)
        elif event == Characters.CONSULTUM:
            self.senatusListen(character, i)
        elif event == Characters.EXILE:
            self.exileListen(character, i)
        elif event == Characters.TRIBAL:
            self.tribalListen(character, i)


    def reset(self, player:Characters.Player):
        for unit in player.units:
            unit.available = True
        self.updateUnits(player)
        player.resetCount()
        self.Handle(player, "resetDone")
        
    #preturn abilities
    #-------------------------------------------------------------------------------------
    def servileListen(self, data):
        sid = flask.request.sid
        character:Characters.Spartacus = self.room.clients[sid]
        #input 1 if player wishes to skip main phase and increase damage by 1
        i = data["i"]
        if i == 1:
            character.revolted = True
        self.Handle(character, "preTurnDone")

    def tribalListen(self, character:Characters.Player, i):
        if i == 1:
            self.showQuote(character, 0)
            self.heal(character, -1)
            for i in range(len(character.units)):
                if isinstance(character.units[i], u.Celtic) or character.units[i].type == u.AUX:
                    self.restore(character, i ,1)
        self.Handle(character, "preTurnDone")
        
    def exileListen(self, player:Characters.Player, i):
        if i == 0:
            self.Handle(player, "preTurnDone")
        else:
            self.showQuote(player, 1)
            self.drawCard(player, 3)
            self.heal(player, 1)         
            self.Handle(player, "postTurnDone")
    #-------------------------------------------------------------------------------------
    def preturn(self, player:Characters.Player):
        self.addDialogue(f"{player.name}'s preparation phase")
        if player.name == "Marius" and len(player.hand) <= 2:
            self.destroyInput(player, [], Characters.EXILE, ["No", "Yes"])
            return        
        if player.name == "Vercingetorix" and any(isinstance(unit, u.Celtic) or unit.type == u.AUX for unit in player.units):   
            self.destroyInput(player, [], Characters.TRIBAL, ["No", "Yes"])
            return
        """
        elif isinstance(player, Characters.Cicero):
            pass
            healingHP = 0
            for i in range(len(player.units)):
                if player.units[i].type == u.MAIN: 
                    if self.reveal(player) %3!=0:
                        healingHP+=1
            if healingHP!=0:
                self.heal(player.sid, healingHP)
            
        elif isinstance(player, Characters.Octavius) and not player.awaken:
            pass
            if player.hp<=4:
                self.drawCard(player,1)
                self.heal(player, 1)
                player.PoliticalLimit = 100
                player.awaken = True

        elif isinstance(player, Characters.Vercingetorix):
            pass
            n = []
            for i in range(len(player.units)):
                if isinstance(player.units[i], u.Celtic) or player.units[i].type == u.AUX:
                    n.append(i)
            if len(n):
                self.room.send("tribalInput", {"n":n}, player.sid)
                return

        if isinstance(player, Characters.Spartacus):
            pass
            self.room.send("servileInput",{}, player.sid)
            return
        """
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
        if player.states['sieged']:
            self.updateStates(player, 'sieged', False)
            self.Handle(player, "drawPhaseDone")
            return
        self.addDialogue(f"{player.name}'s draw phase")
        
        if player.name == 'Octavius' and player.awaken:
            self.drawCard(player, 3)
        elif player.name == 'Crassus':
            if len(player.opp.hand):
                self.showQuote(player, 1)
                self.drawCard(player, 1)
                self.playInput(player.opp, [i for i in range(len(player.opp.hand))], Characters.CREDITOR)
                return
            
        else:
            self.drawCard(player, 2)
        self.addDialogue(f"{player.name}'s play phase")

        self.Handle(player, "drawPhaseDone")

    def playphaseListen(self, character, i):
        card = character.hand[i]
        #self.showCard(character, card, "Card Played")
        del character.hand[i]
        self.updateHand(character)
        self.playCard(character, card)

    def playphase(self, player:Characters.Player):
        if player.states['panem']:
            self.updateStates(player, 'panem', False)
            self.Handle(player, "battlePhaseDone")
            return
        n = []
        #check playable cards
        for i in range(len(player.hand)):
            if self.checkCardAvailable(player, player.hand[i]):
                n.append(i)
        if len(n):
            self.playInput(player, n, Characters.PLAY, choices=["cancel"])
            return
        self.Handle(player, "playPhaseDone")

    def discardphase(self, player:Characters.Player):
        if isinstance(player, Characters.Crassus) and len(player.hand) >= 5:
            self.showQuote(player, 0)
        if len(player.hand) - player.handLimit > 0:
            self.addDialogue(f"{player.name}'s discard phase")
            player.discard_event = "discardPhaseDone"
            player.discard = len(player.hand) - player.handLimit
            self.discardCard(player)
            return
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
        
    #player: player dealing damage
    def attackSuccess(self, player:Characters.Player):
        main_u = player.units[player.main]
        n = []
        if player.name == '#Sulla':
            for i in range(len(player.opp.units)):
                if player.opp.units[i].ap <= player.dp:
                    n.append(i)
            self.room.send("diplomatInput", {"n":n}, player.sid)
            return
        if isinstance(main_u, u.Cavalry):
            if isinstance(player, Characters.Pompeius):
                self.showQuote(player, 1)
                self.heal(player, 2)
        if isinstance(main_u, u.Elephant):
            for i in range(len(player.opp.units)):
                if player.opp.units[i].ap <= 1:
                    n.append(i)
            self.room.send("elephantInput", {"n":n}, player.sid)
            return
        if isinstance(main_u, u.Celtic):
            self.showQuote(player, 1)
            self.heal(player, 1)
        self.attackDamage(player.opp)
        
    #player: player receiving damage
    def attackDamage(self, player:Characters.Player):        
        self.dealDamage(player, player.opp.dp)

        if any([isinstance(unit, u.Elephant) for unit in player.units]) and isinstance(player.opp.units[player.opp.main], u.Archery):
            for i in range(len(player.units)):
                self.remove(player, i, 1)
        
        self.Handle(player.opp, "battlePhaseDone")
    
    def defendListen(self, character, i):
        self.addDialogue(f"{character.name} defended with [shield]")
        del character.hand[i] 
        self.updateHand(character)
        character.df -= 1
        if character.df == 0:
            self.Handle(character.opp, "battlePhaseDone")
            return
        self.defend(character)

    def defend(self, player:Characters.Player):
        n = []
        for i in range(len(player.hand)):
            if isinstance(player.hand[i], c.Shield):
                n.append(i)
        self.playInput(player, n, Characters.DEFEND, choices=['cancel'])
        
    def attack(self, player:Characters.Player):
        main_u = player.units[player.main]
        player.dp = 2
        self.addDialogue(f"{player.name} attacked with <{main_u.name}>")
        if isinstance(player, Characters.Surena) and len(player.opp.hand) > len(player.hand):
            player.dp += 1
            self.addDialogue(player, 0)

        elif player.name == 'Caesar':
            if self.reveal(player) % 2 == 0:
                self.showQuote(player, 0)
                player.dp += 1

        elif player.name == '#Spartacus' and player.revolted:    
            player.dp += 1

        if player.opp.name == 'Caesar' and len(player.units) > len(player.opp.units):
            self.showQuote(player.opp, 0)
            self.drawCard(player.opp, 1)

        if isinstance(main_u, u.Archery):
            player.dp -= 1
            if isinstance(main_u, u.Mounted_Archer) and player.opp.hp >= 6:
                player.dp += 1
            self.attackSuccess(player)
            return
        
        def_n = 1
        dis_n = 0
        if isinstance(main_u, u.Cavalry) and player.opp.hp >= 6:
            player.dp += 1
            
        if player.aux >= 0:
            aux_u = player.units[player.aux]
            self.addDialogue(f"{player.name} is assisted by their <{aux_u.name}> auxiliaries")
            def_n += isinstance(aux_u, u.Velite)
            dis_n += isinstance(aux_u, u.Slinger)
        def_n +=  isinstance(main_u, u.Gladiator)
        dis_n += isinstance(main_u, u.Phalanx)
        player.opp.df = def_n
        player.opp.discard = dis_n
        if dis_n:
            player.opp.discard_event = "battle"
            self.discardCard(player.opp)
            return
        self.defend(player.opp)
       
    def auxListen(self, character, i):
        character.aux = i
        self.attack(character)
                
    #main, aux are the indices of the chosen units
    def battlephaseListen(self, character:Characters.Player, i):
        #select auxiliary unit
        character.main = i
        if isinstance(character.units[i], u.Legionary):
            n = []
            for index in range(len(character.units)):
                if character.units[index].type == u.AUX and character.units[index].available:
                    n.append(index)
            if len(n):
                self.deployInput(character, n, Characters.DEPLOY_AUX, ['cancel'])
                return
        self.attack(character)

    def battlephase(self, player:Characters.Player):
        self.addDialogue(f"{player.name}'s battle phase")
        n = []
        for i in range(len(player.units)):
            if player.units[i].type == u.MAIN and player.units[i].available:
                n.append(i)
        if len(n):
            self.deployInput(player, n, Characters.DEPLOY_MAIN, ['cancel'])
            return
        self.Handle(player, "battlePhaseDone")

    def postturn(self, player : Characters.Player):
        self.addDialogue(f"{player.name}'s end phase")
        if isinstance(player, Characters.Sulla):
            #insert character logic
            pass
        elif isinstance(player.opp, Characters.Cicero) and player.opp.accusation and len(player.hand) > 0:
            if self.reveal(player) % 3 == 0:
                player.opp.discard = len(player.opp.hand)
                player.opp.discard_event = "battlePhaseDone"
                self.discardCard(player.opp)
                return
        self.Handle(player, "postTurnDone")
    
if __name__ == "__main__":
    g = GameManager()
