from threading import Event
from PIL import Image
from . import Card

def makeCharacterCard(character:str):
    return Card.CharacterCard(character)

#make game object for UI
class Game:
    def __init__(self):
        pass

    #on receiving playTurn, UI starts internal functions for preturn, drawphase, ...
    def playTurn(self):
        pass

    #create function to draw cards (sending a request to the server) at the beginning of each turn
    #convert to Card object

    #if card number in hand exceeds 4, ask for discard phase