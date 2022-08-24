from PIL import Image
#from . import Card
import Card

def makeCharacterCard(character:str):
    return Card.CharacterCard(character)

if __name__ == "__main__":
    card = makeCharacterCard("Julius Caesar")
    print(card.image)