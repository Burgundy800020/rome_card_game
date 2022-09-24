from threading import Event
from PIL import Image
from . import Card

def makeCharacterCard(character:str):
    return Card.CharacterCard(character)

class Game:
    def __init__(self, socketIO, id):
        self.sio = socketIO
        self.id = id

        self.hand = [] #hand of cards containing a list of Card object
    
    def parseCards(self, hand):
        for card in hand:
            newcard = Card.Card()
            newcard.fromJson(card)
            self.hand.append(newcard)

    def preturn(self):
        pass
        
    def drawphase(self):
        self.sio.emit(f"{id}/drawCard", data={"n":2}, callback=self.parseCards)

    def playphase(self):
        pass

    def discardCards(self, n:list):
        if len(self.hand) <= 4:
            #don't need to discard if there are less than 5 cards in hand
            return
        self.sio.emit(f"{id}/discardCard", data={"n":n}, callback=self.parseCards)

    def attackphase(self):
        pass

    def postturn(self):
        pass