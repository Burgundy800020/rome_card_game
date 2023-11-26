from random import choices
from . import Card as c, Unit as u
#import Card as c

#play_event
PLAY = 1
DISCARD = 2
DEFEND = 3
TESTUDO = 4
VETO = 5

#deploy_event
DEPLOY_MAIN = 11
DEPLOY_AUX = 12
BOOST = 13
AQUILIFER = 14
CAMP = 15
#destroy_event
BARBARIAN = 21
CONSULTUM = 22
EXILE = 301
TRIBAL = 302



class Player:
    
    name = ""
    full = ''
    quotes = []
    abilities = []
    

    def __init__(self, game, sid=""):

        self.game = game
        self.sid = sid

        self.opp : Player = None
        self.hp = 10
        self.hand = []
        self.units = []
        
        #cards
        self.military : c.Card = None
        self.political : c.Card = None

        #events
        self.play_event = 0
        self.deploy_event = 0
        self.destroy_event = 0
        self.choose_event = 0

        #discard
        self.discard = 0
        self.discard_event = ''
        self.dc = 0
        self.df = 0

        #battle
        self.main = -1
        self.aux = -1
        self.dp = 2

        #counters
        self.itemLimit = self.PoliticalLimit = 1
        self.itemPlayed = self.PoliticalPlayed = 0
        self.handLimit = 4

        self.states = {'sieged':False, 'panem':False, 'proscriptio':False}
    
    def resetCard(self):
        self.military = None
        self.political = None

    def resetEvent(self):
        self.play_event = 0
        self.deploy_event = 0
        self.destroy_event = 0
        self.choose_event = 0
    
    def resetCount(self):
        #reset counters for item cards and strategy cards played during a turn
        self.itemPlayed = self.PoliticalPlayed = 0
        self.dp = 2
        self.main = self.aux = -1
    def unitsToJson(self):
        return [unit.toJson() for unit in self.units]

    def handToJson(self):
        return [card.toJson() for card in self.hand]

    def toJson(self):
        return {"name":self.name}

class Marius(Player):

    name = "Marius"
    full = "Caius Marius"
    abilities = ["Permanent Army", "Exile"]
    quotes = [["The law speaks too softly to be heard admist the din of arms",
              "Do not trouble yourself for your brethren, for we have already provided lands for them"],
              ["The exile is temporary, the return is inevitable"] 
              ]

    def __init__(self, game, **kwargs):
        super(Marius, self).__init__(game, **kwargs)
        
class Sulla(Player):

    name = "Sulla"
    full = "Lucius Cornelius Sulla"
    quotes = [
        [
            ""
        ]
    ]

    def __init__(self, game, **kwargs):
        super(Sulla, self).__init__(game, **kwargs)

class Cicero(Player):

    name = "Cicero"
    full = "Marcus Tullius Cicero"
    def __init__(self, game, **kwargs):
        super(Cicero, self).__init__(game, **kwargs)
        self.accusation = False
    def resetCount(self):
        super(Cicero, self).resetCount()
        self.accusation = False

class Crassus(Player):

    name = "Crassus"
    full = "Marcius Lucinius Crassus"
    quotes = [
            [
                "Greed is but a word jealous man inflict upon the ambitious", 
                "My tastes include both snails and oysters"
            ],
            ["The disadvantage of being a Patrician is that occasionally you are obliged to act like one"]
        ]

    def __init__(self, game, **kwargs):
        super(Crassus, self).__init__(game, **kwargs)
        self.handLimit = 5

class Caesar(Player):
    
    name = "Caesar"
    full = "Caius Julius Caesar"
    abilities = ["Tactician", "Dictator Perpetuo"]
    quotes = [
        [
            "Alea jecta est!", "I love the name of honor more than I fear death"
        ],
        ["Non sum rex, sed Caesar", "I am prepared to resort to anything for the sake of Rome"]
    ]

    def __init__(self, game, **kwargs):
        super(Caesar, self).__init__(game, **kwargs)
        self.PoliticalLimit = 100

class Pompeius(Player):

    name = "Pompeius" 
    full = "Gnaeus Pompeius Magnus"
    abilities = ["Great Conqueror", "Vir Triumphalis"]
    quotes = [
        [
            "Stop quoting laws, we carry weapons", "To navigate is necessary, to live is not"
        ],
        ["I brought the whole world in my three triumphs"]
    ]

    def __init__(self, game, **kwargs):
        super(Pompeius, self).__init__(game, **kwargs)

class Octavius(Player):
    
    name = "Octavius" 
    full = "Caius Octavius"
    def __init__(self, game, **kwargs):
        super(Pompeius, self).__init__(game, **kwargs)


class Vercingetorix(Player):
    
    name = "Vercingetorix" 
    full = "Vercingetorix" 
    abilities = ["Tribal Alliance", "Celtic Warrior"]
    quotes = [
        [
            "Under the rising sun I see the peoples of Gaul united",
            "I am a king, appointed by destiny"
        ],
        ["You want to fight? You want to live forever? Then I will lead you"]
    ]

    def __init__(self, game, **kwargs):
        super(Vercingetorix, self).__init__(game, **kwargs)

class Mithridates(Player):
    
    name = "Mithridates" 
    full = "Mithridates VI of Pontus" 

    def __init__(self, game, **kwargs):
        super(Mithridates, self).__init__(game, **kwargs)
        self.immune = False
    def resetCount(self):
        super(Mithridates, self).resetCount()
        self.immune = False
        
class Surena(Player):
    
    name = "Surena" 
    full = "Surena" 

    abilities = ["Heroism", "Mounted Archer"]

    quotes = [
        [
            "He who would be serene and pure needs but one thing, detachment",
            "Our enemies conquer for gold, and they will perish because of gold"
        ],
        ["None surpasses in skill the Parthian mounted archers"]
    ]

    def __init__(self, game, **kwargs):
        super(Surena, self).__init__(game, **kwargs)

class Spartacus(Player):
    
    name = "Spartacus" 
    full = "Spartacus" 

    abilities = ["Servile Revolt", "Gladiator"]
    quotes = [
        [
            "We will live free, or join our brothers in death",
            "Gladiators seek to best all, it is how they survive"
        ]
    ]
    revolted = False
    def __init__(self, game, **kwargs):
        super(Spartacus, self).__init__(game, **kwargs)
    def resetCount(self):
        super(Spartacus, self).resetCount()
        self.revolted = False

characterList = [Marius, Caesar, Vercingetorix, Pompeius]
#[Caesar, Vercingetorix, Pompeius, Crassus, Spartacus, Surena]
nameList = [p.name for p in characterList]

