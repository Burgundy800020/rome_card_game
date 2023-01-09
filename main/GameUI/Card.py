from random import randint
if __package__ is None or __package__ == "":
    from fileControl import readDescription, readImage
else:
    from .fileControl import readDescription, readImage

class Card:
    def __init__(self):
        self.numeral = randint(1, 6)
        self.available = True

    def toJson(self):
        #convert card into json format
        return {
            "type":self.type,
            "numeral":self.numeral,
            "available":self.available}
    
    def fromJson(self, data):
        #load card information from json data
        self.type = data["type"]
        self.numeral = data["numeral"]
        self.available = data["available"]

class CharacterCard:
    def __init__(self, character:str):
        self.name = character
        self.image = readImage(character)
        self.description = readDescription(character)
