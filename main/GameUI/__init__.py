import zipfile, io
from PIL import Image

archive = zipfile.ZipFile("sources.zip", "r")

def readImage(name:str, source=archive):
    #fetch source archive for card image using class name
    #return image in bytes format
    return io.BytesIO(source.read(f"{name}.jpg"))