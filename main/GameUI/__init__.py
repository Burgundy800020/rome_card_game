#relative import only when file is used as a package
if __package__ is None or __package__ == "":
    import Card
    from fileControl import readImage
else:
    from . import Card
    from .fileControl import readImage

def makeCharacterCard(character:str):
    return Card.CharacterCard(character)

def getImage(character:str):
    return readImage(character)

class Game:
    def __init__(self):
        self.hand = [] #player's hand of card
    
    def setHand(self, hand):
        self.hand = [Card.Card().fromJson(card) for card in hand]