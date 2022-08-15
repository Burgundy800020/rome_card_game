import zipfile, io
from PIL import Image
from . import Card

archive = zipfile.ZipFile("sources.zip", "r")

def readImage(name:str, source=archive) -> bytes:
    #fetch source archive for card image using class name
    #return image in bytes format
    data = io.BytesIO(source.read(f"{name}.jpg"))
    data.seek(0)
    return data.read()

def makeCharacterCard(character:str):
    return Card.Card(character)