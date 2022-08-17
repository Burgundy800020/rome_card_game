import zipfile, io

archive = zipfile.ZipFile("sources.zip", "r")

def readImage(name:str, source=archive) -> bytes:
    #fetch source archive for card image using class name
    #return image in bytes format
    data = io.BytesIO(source.read(f"{name}.png"))
    data.seek(0)
    return data.read()

class CharacterCard:
    def __init__(self, character:str):
        self.name = character
        self.image = readImage("soldier")