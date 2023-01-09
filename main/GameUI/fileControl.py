import json, zipfile, io
from PIL import Image
import numpy as np

archive = zipfile.ZipFile("assets/sources.zip", "r")

def readImage(name:str, source=archive) -> np.array:
    #fetch source archive for card image using class name
    #return image in bytes format
    try:data = io.BytesIO(source.read(f"{name}.png"))
    except:data = io.BytesIO(source.read("Soldier.png"))
    data.seek(0)
    
    #transform to numpy array
    image = Image.open(data).convert("RGBA")
    return np.flipud(np.array(image, dtype=np.uint8))

def readDescription(name:str, source=archive) -> str:
    #fetch character description in the file 'description.json'
    #return a string
    descriptions = json.load(io.BytesIO(source.read("descriptions.json")))
    return descriptions.get(name, "A description of this character is coming soon")