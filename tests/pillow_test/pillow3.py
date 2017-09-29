"""
Run this script with the image filenames as arguments.
example: python pillow2.py image.jpg
"""
import os, sys
from PIL import Image

BOX = (420, 120, 1380, 1080)

print("Pillow test script starting...")

for infile in sys.argv[1:]:
    outfile = os.path.splitext(infile)[0] + "_square.jpg"
    if infile != outfile:
        try:
            im = Image.open(infile)
            square = im.crop(BOX)
            square.save(outfile, "JPEG")
            print(outfile, " saved!")
            print(square.format, square.size, square.mode)
        except IOError:
            print("cannot create thumbnail for", infile)

print("Pillow test script finished...")
