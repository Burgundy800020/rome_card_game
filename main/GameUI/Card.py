import zipfile, io
from PIL import Image
import numpy as np

archive = zipfile.ZipFile("sources.zip", "r")

def readImage(name:str, source=archive) -> np.array:
    #fetch source archive for card image using class name
    #return image in bytes format
    data = io.BytesIO(source.read(f"{name}.png"))
    data.seek(0)
    
    #transform to numpy array
    image = Image.open(data).convert("RGBA")
    return np.array(image)

class CharacterCard:
    def __init__(self, character:str):
        self.name = character
        self.image = readImage("soldier")
        self.description = "This is a very very long string to test text."