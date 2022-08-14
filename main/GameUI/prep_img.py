from PIL import Image
import sys, zipfile, io

file = sys.argv[1]
archive = zipfile.ZipFile("sources.zip", "w")

image = Image.open(file)
image = image.resize((150, 200))

image_bytes = io.BytesIO()
file_png = ".".join(file.split(".")[:-1])+ ".png"
image.save("file.png", format="png")
image.save(image_bytes, format="png")
#print(image_bytes.read())

with archive.open(file_png, "w") as file:
    file.write(image_bytes.read())
    file.close()
