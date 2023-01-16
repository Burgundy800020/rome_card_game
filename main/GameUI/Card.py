from random import randint
if __package__ is None or __package__ == "":
    from fileControl import readDescription, readImage
else:
    from .fileControl import readDescription, readImage

class Card:
    def __init__(self, name = ""):
        self.numeral = randint(1, 6)
        self.name = name
        self.type = None
        self.available = False

    def toJson(self):
        #convert card into json format
        return {
            "name":self.name,
            "numeral":self.numeral,
            "type":self.type
            }
    
    def fromJson(self, data):
        #load card information from json data
        self.name = data["name"]
        self.numeral = data["numeral"]
        self.type = data["type"]

class CharacterCard:
    def __init__(self, character:str):
        self.name = character
        self.image = readImage(character)
        self.description = readDescription(character)
